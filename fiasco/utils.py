from random import choice

def make_salt():
	chars = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!@#$%^&*()_-=+"
	return ''.join(choice(chars) for i in range(24))

def logged_in(session):
	s_keys = session.keys()
	if not 'logged_in' in s_keys:
		return False
	if session['logged_in'] == True:
		return True
	if not 'username' in s_keys or not 'uid' in s_keys:
		return False
	if session['logged_in'] == True:
		return True

	return False

def unpack_details(details):
	form_dict = {}
	for detail in details:
		if detail.detail_type not in form_dict.keys():
			form_dict[detail.detail_type] = {}

		for head in detail.data.headers.items():
			h_key = head[0]
			h_val = head[1]
			h_field_name = 'rel_head_' + str(h_key)
			h_field_content = h_val
			form_dict[detail.detail_type][h_field_name] = h_field_content
			count = 0
			for field in detail.data.data[h_key]:
				count += 1
				f_field_name = "rel_%s_%s" % (h_key, count)
				f_field_content = field
				form_dict[detail.detail_type][f_field_name] = f_field_content

	return form_dict


