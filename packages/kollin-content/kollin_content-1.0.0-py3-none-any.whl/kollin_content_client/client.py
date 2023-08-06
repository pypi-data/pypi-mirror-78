import requests
import json


def flatten(l): return [item for sublist in l for item in sublist]


class KollinApiClient:
    def __init__(self, api_url, email, password):
        super().__init__()
        self.tokens = None
        self.api_url = api_url
        raw_tokens = self.login(email, password)
        self.tokens = {
            "x-refresh-token": raw_tokens["refreshToken"], "x-token": raw_tokens["token"]}

    def gql_query(self, body):
        return self.gql_request("query", body)

    def gql_mutation(self, body):
        return self.gql_request("mutation", body)

    def login(self, email, password):
        login_mutation = f"""login(email:"{email}",password:"{password}"){{
            token
            refreshToken
        }}
        """
        tokens = self.gql_mutation(login_mutation)
        return tokens

    def gql_request(self, request_type, body):
        body = f"""{request_type} {{ {body} }}"""
        if self.tokens != None:
            headers = self.tokens
        else:
            headers = {}
        r = requests.post(self.api_url, json={'query': body}, headers=headers)
        if r.status_code != 200:
            print(r.text)
        response_dict = json.loads(r.text)
        data_dict = response_dict["data"]
        return data_dict[list(data_dict.keys())[0]]


# TODO : getCourseTagVotes returns tag votes with tags from outside the course

    def get_course_exercises_with_labels(self, course_id):
        """
        From the given course, get all exercises from course along with it's metadata.
        A label (tag or module) needs to be validated in order to be counted.

        Args:
            course_id (int): id of the course

        Returns:
            labelled_exercises (list of dicts): each dict has following structure:
            {
            id:string,
            name:string,
            text:string,
            tags:,
            [
                {id:string,name:string},
            ],
            modules:
            [
                {id:string,name:string},
            ],
            }
        """

        tag_votes_query = f"""
            getCourseTagVotes(courseId:{course_id})
            {{
                exerciseId
                tagId
                validated

            }}

        """
        tag_votes = self.gql_query(tag_votes_query)

        course_query = f"""
        getCourse(id:{course_id})
        {{
            id
            modules {{
                id
                name
                tags{{
                    id
                    name
                }}
            }}
            exercises{{
                id
                text
                solution{{
                    id
                    text
                }}
                tags{{
                    id
                    name
                    module(course_id:{course_id}){{
                        id
                        name
                    }}
                }}
            }}
        }}

        """
        # fetch and reformat tag data

        course = self.gql_query(course_query)

        tags = [{**t, "module_id": m["id"]}
                for m in course["modules"] for t in m["tags"]]
        tag_id2module_id = {}

        for module in course["modules"]:
            for tag in module["tags"]:
                tag_id2module_id[tag["id"]] = module["id"]

        course = {**course, "tags": tags}

        # organize exercise data

        exercises = course["exercises"]
        exercises = [{**e, "modules": [t["module"]
                                       for t in e["tags"]]} for e in exercises]
        n_exercises = len(exercises)
        exercise_ids = [e["id"] for e in exercises]
        exercise_id2idx = {
            exercise_id: idx for idx, exercise_id in enumerate(exercise_ids)}

        for exercise_id in exercise_ids:
            assert exercise_ids[exercise_id2idx[exercise_id]] == exercise_id

        exercise_texts = [str(e["text"])+" "+str(e["solution"]
                                                 ["text"] if e["solution"] else "") for e in exercises]
        exercise_id2text = {exercise_id: exercise_text for exercise_id,
                            exercise_text in zip(exercise_ids, exercise_texts)}

        for exercise_id in exercise_ids:
            assert exercise_id2text[exercise_id] == exercise_texts[exercise_id2idx[exercise_id]]

        # initialize exercise dicts

        labelled_exercises = {}

        for exercise_id, exercise_text in zip(exercise_ids, exercise_texts):
            labelled_exercises[exercise_id] = {
                "id": exercise_id, "text": exercise_text, "tags": {}, "modules": {}}

        # populate exercise dicts

        for label_type in ["modules", "tags"]:

            labels = course[label_type]
            n_labels = len(labels)
            label_ids = [label["id"] for label in labels]
            label_id2idx = {label_id: idx for idx,
                            label_id in enumerate(label_ids)}
            label_names = [label["name"] for label in labels]

            for label_id in label_ids:
                assert label_ids[label_id2idx[label_id]] == label_id

            for tv in tag_votes:
                if bool(tv["validated"]) == True and tv["tagId"] in tag_id2module_id:
                    if label_type == "modules":
                        label_id = tag_id2module_id[tv["tagId"]]
                    elif label_type == "tags":
                        label_id = tv["tagId"]

                    exercise_id = tv["exerciseId"]
                    labelled_exercises[exercise_id][label_type][label_id] = {
                        "id": label_id, "name": label_names[label_id2idx[label_id]]}

            for exercise_id in labelled_exercises.keys():
                labelled_exercises[exercise_id][label_type] = list(
                    labelled_exercises[exercise_id][label_type].values())

        return list(labelled_exercises.values())

    def get_course_label_theory(self, course_id, label_type):
        """get dictionnary relating label ids to theory text. Labels can be either modules or tags.

        Args:
            course_id (int): id of course
            label_type (string): "module" or "tag"

        Returns:
            label_id2label_theory (dict): dictionnary which maps between label ids and label theory text
        """
        assert (label_type == "tag" or label_type == "module")

        query = f"""
        getCourse(id:{course_id}){{
            id
            modules{{
                id
                name
                tags{{
                    id
                    name
                    chapters{{
                        id
                        markdown
                    }}
                }}
            }}
        }}
        """
        course = self.gql_query(query)
        modules = course["modules"]
        tags = flatten([module["tags"] for module in modules])
        tag_id2tag_theory = {tag["id"]: tag["name"]+" "+" ".join(
            [ch["markdown"] for ch in tag["chapters"]] if tag["chapters"] != None else []) for tag in tags}
        module_id2module_theory = {module["id"]: module["name"]+" "+" ".join(
            [tag_id2tag_theory[tag_id] for tag_id in [tag["id"] for tag in module["tags"]]]) for module in modules}

        if label_type == "module":
            label_id2label_theory = module_id2module_theory
        elif label_type == "tag":
            label_id2label_theory = tag_id2tag_theory
        return label_id2label_theory

    # def get_course_training_data(course_id):

    #     # get all tags in course

    #     # get all courses where tags occur

    #     # get all exercises from each course

    #     return labelled_exercise


client = KollinApiClient()

# labelled_exercises = client.get_course_exercises_with_labels(
#     10)


# label_id2label_theory = client.get_course_label_theory(10, "tag")
