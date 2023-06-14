from django.db import models
from users.models import User
from tgbot.handlers.broadcast_message.utils import send_one_message
import deal_search.modules.deals_client.client as client
from tgbot.handlers.deal_search import static_text

class Provider(models.Model):
    identifier = models.CharField(max_length=10)

class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    provider = models.ForeignKey(Provider, on_delete=models.CASCADE)
    product_id = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    search_type = models.CharField(max_length=10)

    def fetch_items_and_notify(self):
        postings = self._fetch_postings()

        new_postings = self._find_new_postings(postings)

        ## Send telegram notification
        if len(postings) > 0:
            for posting in new_postings:
                text = static_text.result.format(name=posting.name, price=posting.price, branch_name=posting.outlet_name, url=posting.fundgrube_url())
                send_one_message(text=text, user_id=self.user.user_id, disable_web_page_preview=True)
                
                ## Store new found posting_ids    
                IndexedPosting.objects.create(notification=self, posting_id=posting.id)
    
    @classmethod
    def fetch_items_and_notify_all(cls):
        for notification in cls.objects.all():
            notification.fetch_items_and_notify()
    
    def _fetch_postings(self):
        provider = client.Provider(self.provider)

        branch_ids = ','.join([str(branch_selection.branch.branch_id) for branch_selection in BranchSelection.objects.filter(user=self.user).select_related('branch')])

        query_params = {"text": self.product_id, "outletIds": branch_ids}
        query = client.DealsQuery(query_params)
        search = client.DealSearch(provider, query)
        postings = search.postings()

        return postings

    def _find_new_postings(self, postings):
        indexed_posting_ids = self.indexedposting_set.values_list('posting_id', flat=True)

        return [posting for posting in postings if posting.id not in indexed_posting_ids]

class Branch(models.Model):
    name = models.CharField(max_length=255)
    provider = models.ForeignKey(Provider, on_delete=models.CASCADE)
    branch_id = models.IntegerField()
    zip_code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)

    @classmethod
    def sync_remote(cls, provider):
        c_provider = client.Provider(provider.identifier)
        search = client.BranchSearch(provider = c_provider, limit=1000)
        c_branches = search.fetch_branches()

        for branch in c_branches:
            Branch.objects.get_or_create(
                name = branch['displayNameShort'],
                provider = provider,
                branch_id = branch['id'],
                zip_code = branch['address']['zipCode']
            )
        
    class Meta:
        ordering = ["zip_code"]

class BranchSelection(models.Model):
    user =  models.ForeignKey(User, on_delete=models.CASCADE)
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)

class IndexedPosting(models.Model):
    notification = models.ForeignKey(Notification, on_delete=models.CASCADE)
    posting_id = models.CharField(max_length=255)

class Posting(models.Model): 
    provider = models.ForeignKey(Provider, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.TextField()
    posting_id = models.CharField(max_length=36)
    product_id = models.IntegerField()
    price = models.DecimalField(decimal_places=2,max_digits=8)
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE)
    image_url = models.TextField()
    shipping_type = models.CharField(max_length=255)
    shipping_cost = models.DecimalField(decimal_places=2,max_digits=6)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    shop_url = models.CharField(max_length=255)

    @classmethod
    def sync_remote_by_branch(cls, provider, branch):
        c_provider = client.Provider(provider.identifier)
        c_query = client.DealsQuery({"outletIds": branch.branch_id})
        c_search = client.DealSearch(c_provider, c_query)

        c_postings = c_search.postings()

        known_posting_ids = [posting.posting_id for posting in Posting.objects.filter(provider=provider, branch=branch).only('posting_id')]

        created_count = 0
        for c_posting in c_postings:
            if c_posting.id in known_posting_ids:
                continue
            else:
                Posting.objects.create(
                    provider = provider,
                    name = c_posting.name,
                    description = c_posting.text,
                    posting_id = c_posting.id,
                    product_id = c_posting.pim_id,
                    price = c_posting.price,
                    branch = branch,
                    image_url = c_posting.original_url,
                    shipping_type = c_posting.shipping_type,
                    shipping_cost = c_posting.shipping_cost,
                    shop_url = c_posting.fundgrube_url()
                )

                created_count += 1
        
        print(f"Branch {branch.branch_id}: Created {created_count} postings.")

    @classmethod
    def sync_remote(cls):
        for branch in Branch.objects.all():
            cls.sync_remote_by_branch(branch.provider, branch)
