import csv
import time
import smtplib
import dns.resolver


csv_path = 'input.csv'

outputDataFile = "output_data.csv"
write_data = csv.writer(open(outputDataFile, 'a'), delimiter=',')
print("Do not Close file or End Process.")
print("Extracting features from raw data.........")

with open(csv_path, 'r') as csv_file:
    email_data = csv.reader(csv_file)
    i = 0
    for email in email_data:
        test_address = "corn@bt.com"
        email_id = email[0].lower()
        splitAddress = email_id.split('@')
        domain = str(splitAddress[1])
        # print('Domain:', domain)
        records = dns.resolver.query(domain, 'MX')
        mxRecord = records[0].exchange
        mxRecord = str(mxRecord)
        # print(mxRecord)
        try:
            server = smtplib.SMTP()
            server.set_debuglevel(0)
            server.connect(mxRecord)
            server.helo(server.local_hostname)
            server.mail(test_address)
            code, message = server.rcpt(str(email_id))
            if code == 250:
                print(code)
                value = email_id.strip()
                write_data.writerow(value + " is_valid")
            else:
                value = email_id.strip()
                print(value)
                print(message)
                write_data.writerow(value + " is_invalid")
                continue

            time.sleep(2)
            server.quit()
        except TimeoutError as e:
            print(e)