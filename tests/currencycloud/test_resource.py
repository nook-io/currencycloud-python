from currencycloud import Config
from currencycloud.http import Http
from currencycloud.resources.resource import Resource
from mock import patch


class TestResource:
    class PersonClient(Http):
        def delete(self, resource_id):
            pass

        def update(self, resource_id, **kwargs):
            pass

    class Person(Resource):
        pass

    def setup_method(self):
        self.config = Config("dummy", "dummy", Config.ENV_DEMO)
        self.client = TestResource.PersonClient(self.config)

    def test_resource_save_only_updates_changed_records(self):
        person = TestResource.Person(id=1, name="Some", surname="One")

        with patch.object(Http, "post") as person_post:

            def post_check(url, **kargs):
                assert url == 1
                assert len(kargs) == 1
                assert kargs["name"] == "Penelope"

            person_post.side_effect = post_check

            person.name = "Penelope"
            assert person.update() == person

    def test_resource_delete_calls_delete_on_resource(self):
        person = TestResource.Person(id=1, name="Some", surname="One")

        with patch.object(Http, "post") as person_post:

            def post_check(url, **kargs):
                assert url == "1/delete"

            person_post.side_effect = post_check
            person.delete()
