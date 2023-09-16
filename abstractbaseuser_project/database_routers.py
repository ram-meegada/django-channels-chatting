class UserRouter:
    route_app_labels = {"auth", "contenttypes"}
    def db_for_read(self, model, **hints):
        print(model._meta.app_label, 'model._meta.app_labelmodel._meta.app_labelmodel._meta.app_label')
        if model._meta.app_label in self.route_app_labels:
            return 'user_db'
        return None

    def db_for_write(self, model, **hints):
        print(model._meta.app_label, 'model._meta.app_labelmodel._meta.app_labelmodel._meta.app_label')
        if model._meta.app_label in self.route_app_labels:
            return 'user_db'
        return None

    def allow_relation(self, obj1, obj2, **hints):
        if (
            obj1._meta.app_label in self.route_app_labels
            or obj2._meta.app_label in self.route_app_labels
        ):
            return True
        return None
    
    def allow_migrate(self, db, app_label, model_name=None, **hints):
        if app_label in self.route_app_labels:
            return db == 'user_db'
        return None


print('cam to top of OrderRouter=================')
class OrderRouter:
    route_app_labels = {"order_app"}
    def db_for_read(self, model, **hints):
        if model._meta.app_label in self.route_app_labels:
            return "order_db"
        return None

    def db_for_write(self, model, **hints):
        if model._meta.app_label in self.route_app_labels:
            return "order_db"
        return None
    
    # def allow_relation(self, obj1, obj2, **hints):
    #     print(obj1, obj2, '********************objects==============')
    #     if (
    #         obj1._meta.app_label in self.route_app_labels
    #         or obj2._meta.app_label in self.route_app_labels
    #     ):
    #         return True
    #     return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        print(app_label, '=========app_label============')
        if app_label in self.route_app_labels:
            print('came inside*******************')
            return db == "order_db"
        return None
