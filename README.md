# s3_audit
![made-with-python][made-with-python]
![Python Versions][pyversion-button]
[![Hits](https://hits.seeyoufarm.com/api/count/incr/badge.svg?url=https%3A%2F%2Fgithub.com%2Fpassword123456%2Fhit-counter&count_bg=%2379C83D&title_bg=%23555555&icon=&icon_color=%23E7E7E7&title=hits&edge_flat=false)](https://hits.seeyoufarm.com)


[pyversion-button]: https://img.shields.io/pypi/pyversions/Markdown.svg
[made-with-python]: https://img.shields.io/badge/Made%20with-Python-1f425f.svg

- Simple dictionary based read, write, delete permission audit tool for aws s3 bucket written in python.
- Need to aws-cli [(Here get it.)](https://docs.aws.amazon.com/ko_kr/cli/latest/userguide/getting-started-install.html)
- The scan result only show 'true/ false /not given'
- if you see the true flag in the result, have to further scanning or do others ways to find out vulnerability.
- Get the ACL of the S3 bucket using aws credential(access_key method) and fix the vulnerable permission.

# Documentation
```python
# pip install requests
# python main.py
```

# Output
```python
##### Scan Completed ####
1,2022-04-12 19:39:52 yours3domain.s3.ap-northeast-1.amazonaws.com [ListObject: False, PutObject: False, DeleteObject: False]
2,2022-04-12 19:39:56 yours3domain.s3.amazonaws.com [ListObject: False, PutObject: False, DeleteObject: False]

##### This is not S3(?). Make sure domain is correct. ####
1,2022-04-12 19:39:56 nots3domain.com [ListObject: Not_Given, PutObject: Not_Given, DeleteObject: Not_Given]
2,2022-04-12 19:39:56 nots3domain.com [ListObject: Not_Given, PutObject: Not_Given, DeleteObject: Not_Given]
3,2022-04-12 19:39:56 nots3domain.com [ListObject: Not_Given, PutObject: Not_Given, DeleteObject: Not_Given]
4,2022-04-12 19:39:56 nots3domain.com [ListObject: Not_Given, PutObject: Not_Given, DeleteObject: Not_Given]
```
