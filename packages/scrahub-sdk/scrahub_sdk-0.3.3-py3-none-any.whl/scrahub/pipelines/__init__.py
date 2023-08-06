from scrahub.utils import save_item_mongo
from scrahub.utils.config import get_task_id


class ScrahubMongoPipeline(object):
    def process_item(self, item, spider):
        item_dict = dict(item)
        item_dict['task_id'] = get_task_id()
        save_item_mongo(item_dict)

        return item
