import math

class EuclideanDistTracker:
    def __init__(self, dist_limit=25):
        self.center_points = {}
        self.id_count = 0
        self.dist_limit = dist_limit

    def get_centroid(self, rectangle):
        x, y, w, h = rectangle
        cx = (x + x + w) // 2
        cy = (y + y + h) // 2
        return cx, cy

    def calculate_distance(self, c1, c2):
        return math.hypot(c1[0] - c2[0], c1[1] - c2[1])

    def find_existing_object(self, centroid):
        for object_id, center_point in self.center_points.items():
            dist = self.calculate_distance(centroid, center_point)
            if dist < self.dist_limit:
                return object_id
        return None

    def update_existing_object(self, object_id, centroid):
        self.center_points[object_id] = centroid

    def add_new_object(self, centroid):
        self.center_points[self.id_count] = centroid
        new_object_id = self.id_count
        self.id_count += 1
        return new_object_id

    def update(self, objects_rect):
        objects_bbs_ids = []

        for rect in objects_rect:
            centroid = self.get_centroid(rect)
            existing_object_id = self.find_existing_object(centroid)

            if existing_object_id is not None:
                self.update_existing_object(existing_object_id, centroid)
                objects_bbs_ids.append([*rect, existing_object_id])
            else:
                new_object_id = self.add_new_object(centroid)
                objects_bbs_ids.append([*rect, new_object_id])

        self.center_points = {object_id: centroid for object_id, centroid in self.center_points.items() if object_id in {bb_id for _, _, _, _, bb_id in objects_bbs_ids}}

        return objects_bbs_ids

class Filter:
    def __init__(self) -> None:
        self.buf = []
        self.validated = []

    def count_trues_until(self, spot):
        count = 0
        for i in range(spot):
            if self.validated[i] is True:
                count += 1
        return count

    def compare_and_subtract(self, list1, list2):
        # Create a new list to store the results
        result_list = []

        # Determine the length of the shorter list
        min_length = min(len(list1), len(list2))

        # Iterate through the shorter list and compare elements
        for i in range(min_length):
            if list1[i] == list2[i] and (list2[i] >= 0):
                result_list.append(list1[i] - 1)
            else:
                result_list.append(list2[i])

        # Append the remaining elements from the longer list
        if len(list1) > min_length:
            result_list.extend(list1[min_length:])
        elif len(list2) > min_length:
            result_list.extend(list2[min_length:])

        return result_list

    def filter_object(self, objects, limit=10):
        temp_buf = self.buf.copy()
        resulting_objects = []
        for obj in objects:
            if len(self.buf) == obj[-1]:
                self.buf.append(1)
                self.validated.append(False)
            elif len(self.buf) > obj[-1] and self.buf[obj[-1]] < limit:
                self.buf[obj[-1]] += 1
            elif self.buf[obj[-1]] == limit and self.validated[obj[-1]] == False:
                self.validated[obj[-1]] = True
                print(f"Element {obj[-1]} validated!")
            if self.buf[obj[-1]] > -1 and self.validated[obj[-1]] == True:
                temp = obj
                temp[-1] = self.count_trues_until(obj[-1])
                resulting_objects.append(temp)
                #print(f"Object {obj} is ID: {self.count_trues_until(obj[-1])}")
        self.buf = self.compare_and_subtract(temp_buf, self.buf)
        print(resulting_objects)
        return resulting_objects
