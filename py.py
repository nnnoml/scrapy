# -*- coding: utf-8 -*-
a = {7:['s001','s002','s027']}

for idx in a:
	if 'S027'.lower() in a[idx]:
		print(idx)
		break

print(a)