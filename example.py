import katosc
import time

kat =  katosc.KatOsc()

messages = [
    "Hello",
    "three\nlines\ntext",
    "5\nline\ntxt\n4\n5",
    "This is a longer test message",
    "1234567890"*3 + "##*",
    "",
]

def run():
    for msg in messages:
        print("sending:")
        print(msg)

        kat.set_text(msg)
        time.sleep(3)

    print("char limit 128 exceeded")
    kat.set_text("1234567890"*12 + "12345#abcdefghij" )
    time.sleep(12)

run()
kat.stop()
