from django.db import models
from users.models import User
from tgbot.handlers.broadcast_message.utils import send_one_message
import deal_search.modules.deals_client.client as client
from tgbot.handlers.deal_search import static_text

class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    provider = models.CharField(max_length=10)
    product_id = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    search_type = models.CharField(max_length=10)

    def fetch_items_and_notify(self):
        postings = self._fetch_postings()

        new_postings = self._find_new_postings(postings)

        print(new_postings)

        ## Send telegram notification
        for posting in new_postings:
            text = static_text.result.format(name=posting.name, price=posting.price, branch_name=posting.outlet_name, url=posting.fundgrube_url())
            send_one_message(text=text, user_id=self.user.user_id, disable_web_page_preview=True)

        ## Store new found posting_ids
        for posting in new_postings:
            IndexedPosting.objects.create(notification=self, posting_id=posting.id)
    
    @classmethod
    def fetch_items_and_notify_all(cls):
        for notification in cls.objects.all():
            notification.fetch_items_and_notify()
    
    def _fetch_postings(self):
        provider = client.Provider(self.provider)
        outlet_ids = ','.join([str(branch_id) for branch_id in self.user.branch_set.values_list('branch_id', flat=True)])

        query_params = {"text": self.product_id, "outletIds": outlet_ids}
        query = client.DealsQuery(query_params)
        search = client.DealSearch(provider, query)
        postings = search.postings()

        return postings

    def _find_new_postings(self, postings):
        indexed_posting_ids = self.indexedposting_set.values_list('posting_id', flat=True)

        return [posting for posting in postings if posting.id not in indexed_posting_ids]

class Branch(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    provider = models.CharField(max_length=10)
    branch_id = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)

class IndexedPosting(models.Model):
    notification = models.ForeignKey(Notification, on_delete=models.CASCADE)
    posting_id = models.CharField(max_length=255)
