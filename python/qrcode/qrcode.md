
```python
#!/usr/bin/env python
import qrcode

qr = qrcode.QRCode(
    # version=1,
    error_correction=qrcode.constants.ERROR_CORRECT_L,
    # box_size=10,
    border=0,
)

data = """
BEGIN:VCARD
VERSION:4.0
N:Rogers;Mark;M.;Dr.;PhD
FN: Mark Rogers
EMAIL;WORK:mark.rogers@aol.com
TEL;work;pref:+1-111-111-1111
TEL;mobile:+1-222-222-2222
ORG:Americal Online
TITLE:Computer Engineer
URL;work:https://aol.com
URL;homepage:https://mark.rogers.github.io/
END:VCARD
"""

qr.add_data(data)
qr.make(fit=True)

img = qr.make_image(fill_color="grey", back_color="white")
img.save("qrcode.png")
```







