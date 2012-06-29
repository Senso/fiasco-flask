

class Detail(object):
    """ Object representing a set of Details. """

    def __init__(self):
        self.possible_types = ('need', 'location', 'object', 'relationship')
        self.detail_type = None

        self.headers = {1: "", 2: "", 3: "", 4: "", 5: "", 6: ""}

        # uglily init a dict of lists of empty strings
        self.data = dict([[x, ['' for n in range(0, 6)]] for x in range(1, 7)])

        self.unpacked = {}

    def unpack(self):
        #form_dict = {}
        for head in self.headers.items():
            h_key = head[0]
            h_val = head[1]
            h_field_name = "rel_head_%s" % h_key
            h_field_content = h_val
            self.unpacked[h_field_name] = h_field_content
            count = 0
            for field in self.data[h_key]:
                count += 1
                f_field_name = "rel_%s_%s" % (h_key, count)
                f_field_content = field
                self.unpacked[f_field_name] = f_field_content
        #return form_dict
