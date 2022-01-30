import threading

from purdue_brain.common.utils import get_attribute
from purdue_brain.feature.nessie import Nessie
from purdue_brain.wrappers.discord_wrapper import DiscordWrapper


class UserIterator:

    def __init__(self, iterate_property=None):
        self.callback_done = threading.Event()
        self.user_property = dict()
        self.iterate_property = iterate_property
        self.on_database_change()

    def clear_user_property(self):
        for k, _ in self.user_property.items():
            self.user_property[k]['exists'] = False

    def remove_non_exists_data(self):
        for k, v in self.user_property.items():
            if not v['exists']:
                self.user_property.pop(k)

    def on_database_change(self):
        def snapshot(doc_snapshot, changes, read_time):
            self.clear_user_property()
            for doc in doc_snapshot:
                user_dict = {'exists': True, 'data': doc.to_dict()}
                self.user_property[doc.id] = user_dict
            self.remove_non_exists_data()
            self.callback_done.set()

        DiscordWrapper.fire.fireDb.collection('users').on_snapshot(snapshot)

    def __iter__(self):
        for k, v in self.user_property.items():
            nessie_customer_id = get_attribute(v, ['data', 'nessie_customer_id'])
            if nessie_customer_id is not None:
                customer_id, account_id = nessie_customer_id['customer_id'], nessie_customer_id['account_id']
                nessie_object = Nessie(customer_id, account_id)
                yield k, nessie_object
