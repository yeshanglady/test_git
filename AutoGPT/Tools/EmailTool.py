import re
import urllib.parse
import webbrowser
def is_valid_email(email: str)->bool:
    "判断是否为有效的邮箱地址"
    receivers=email.split(";")
    pattern=r"^[a-zA-Z0-9_-]+@[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+)+$"
    for receiver in receivers:
        if not re.match(pattern,receiver):
            return False
    return True

def send_email(
        to: str,
        subject: str,
        body: str,
        cc: str = None,
        bcc: str = None,
) -> str:
    "发送邮件"
    if not is_valid_email(to):
        return "Invalid email address"
    
    #对邮件的主题和正文进行url编码
    subject = urllib.parse.quote(subject)
    body = urllib.parse.quote(body)
    
    #构造mailto链接
    mailto_link = f"mailto:{to}?subject={subject}&body={body}"
    if cc:
        cc=urllib.parse.quote(cc)
        mailto_link += f"&cc={cc}"
    if bcc:
        bcc=urllib.parse.quote(bcc)
        mailto_link += f"&bcc={bcc}"
        
    webbrowser.open(mailto_link)
    return "Email sent successfully"