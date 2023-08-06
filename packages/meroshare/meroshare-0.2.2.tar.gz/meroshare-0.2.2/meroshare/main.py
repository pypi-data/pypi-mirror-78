from meroshare import MeroShare


def main():
	myshare = MeroShare()
	# issues = myshare.getCurrentIssues().issues	
	# for issue in issues:
	# 	print(issue['companyShareId'])

	# 	cid = issue['companyShareId']
	# 	myshare.getCompanyDetails(cid=cid)
	details = myshare.getCompanyDetails(cid='285').printCompanyDetails()
	# myshare.getApplicationReport().printApplicationReport()
	# myshare.eraseCredentials()

if __name__ == '__main__':
	main()
