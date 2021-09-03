import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import pyqtSlot
import pandas as pd
import nltk

# Create Widget
class App(QWidget):         # สร้าง class สำหรับ Application หลักขึ้นมา เป็นการสร้างหน้าต่าง GUI
    def __init__(self):         # สร้างอ๊อบเจคในการกำหนดลักษณะของหน้าต่าง GUI
        super().__init__()      # ส่งคืนอ็อบเจ็กต์ชั่วคราวของซูเปอร์คลาสที่อนุญาตให้เรียกเมธอดของซูเปอร์คลาสนั้น
        self.title = 'ระบบแนะนำประโยค'      # กำหนด title ของโปรแกรม
        self.left = 100     # กำหนดจุดเริ่มต้นของหน้าต่างโปรแกรมกับจอคอมพิวเตอร์ ให้หน้าต่างห่างจากขอบจอด้านซ้าย 100
        self.top = 100      # กำหนดจุดเริ่มต้นของหน้าต่างโปรแกรมกับจอคอมพิวเตอร์ ให้หน้าต่างห่างจากขอบจอด้านบน 100
        self.width = 960        # กำหนดขนาดของหน้าต่างโปรแกรมโดยกำหนดให้มีความยาว 960
        self.height = 720       # กำหนดขนาดของหน้าต่างโปรแกรมโดยกำหนดให้มีความสูง 720
        self.initUI()       # สร้างวิดเจ็ต GUI ทั้งหมดบนหน้าต่าง

    # Create widget ภายในหน้าต่างวินโดว
    def initUI(self):       # สร้างอ๊อบเจค สำหรับสร้างวิดเจ็ดบนหน้าต่าง
        self.setWindowTitle(self.title)         # โปรแกรมแสดงข้อความใน title
        self.setGeometry(self.left, self.top, self.width, self.height)      # หน้าต่างปรากฏตำแหน่งบนจอภาพ

        # ------- นำเข้าคลังข้อมูล ------
        tag_sentence = []       # ประกาศตัวแปรที่มีค่าว่าง
        df = pd.read_csv("store.csv", usecols=["text"])     # อ่านไฟล์ store.CSV โดยเลือกใช้คอลลัมป์ที่มีชื่อว่า text
        for rows in df.values:      # สร้างลูปข้อมูลแต่ละคอลัมน์ และแต่ละแถว มีประโยชน์สำหรับการเขียนฟังก์ชั่นแปลกๆ
            tag_sentence.append(rows[0])        # เพิ่มข้อมูลเข้าไปในลิสต์ tag_sentence ด้วย append ซึ่งข้อมูลที่ถูกเพิ่มเข้าจะอยู่ท้ายสุดและเรียง index เพิ่มขึ้นเรื่อยๆ

        # auto complete options
        names = tag_sentence           # สร้างตัวแปรเพื่อเก็บประโยคทั้งหมด
        completer = QCompleter(names)       # สร้างตัวแปร completer เพื่อตั้งให้เป็น auto completer โดยการเรียกเใช้คำสั่ง QCompleter จากไลบรารี่ PyQt5.QtWidgets

        # Create topic
        self.topic = QLabel(self)       # สร้าง label สำหรับการกำหนดหัวข้อโปรแกรม โดยการเรียกเใช้คำสั่ง QLabel จากไลบรารี PyQt5.QtWidgets
        self.topic.setText('ระบบแนะนำประโยคภาษาอังกฤษโดยใช้การลำดับหน้าที่ของคำ')       # โปรแกรมจะปรากฏหัวข้อโปรแรกมด้วยเมธอด setText
        self.topic.setFont(QFont("supermarket", 16, QFont.Bold))      # กำหนดฟ้อนสำหรับหัวข้อ ขนาดตัวหนังสือ และความหนาบางของตัวหนังสือ โดยเมธอด setFont
        self.topic.move(190, 10)        # กำหนดตำแหน่งของ Label

        # create line edit and add auto complete
        self.lineedit = QLineEdit(self)     # สร้าง textbox โดยการเรียกใช้คำสั่ง QLineEdit เป็นโปรแกรมแก้ไขข้อความบรรทัดเดียว เช่น การลบข้อความ การเลื่อนขึ้นลง การทำซ้ำ มีการรับค่าจากอินพุท
        self.lineedit.move(50,60)       # กำหนดตำแหน่งของช่อง textbox
        self.lineedit.resize(860, 40)       # กำหนดขนาดของ textbox ความยาว ความสูง
        self.lineedit.setCompleter(completer)       #  ดึงตัวแปรที่ถูกเก็บไว้ใน self.lineedit ให้ช่อง textbox เป็นออโต้คอมพลีท โดยการเรียกใช้คำสั่ง setCompleter
        self.lineedit.setFont(QFont('supermarket', 10))       # กำหนดให้ตัวหนังสือที่มีการพิมพ์ภายในช่อง textbox ลักษณะฟ้อน ขนาดตัวหนังสือ และความหนาบางของตัวหนังสือ

        # Create a button in the window
        self.button = QPushButton('Show POS', self)     # สร้างปุ่ม Show POS เพื่อให้ผู้ใช้งานกดดปุ่มเพื่อแสดงประโยคภาษาอังกฤษและการกำกับแท็ก POS
        self.button.move(420, 115)      # กำหนดตำแหน่งของปุ่ม Show POS
        self.button.resize(150, 40)     # กำหนดขนาดของปุ่ม Show POS
        self.button.clicked.connect(self.on_click)      # กำหนดให้หลังจากมีการกดปุุ่ม ให้ทำการ concect ไปที่เมธอด on_click

        # create a label for show text
        self.label = QLabel(self)       # สร้าง label สำหรับการกำหนดพื้นที่แสดงประโยคภาษาอังกฤษ และการกำกับแท็ก POS โดยการเรียกเใช้คำสั่ง QLabel จากไลบรารี PyQt5.QtWidgets
        self.label.move(50, 170)        # กำหนดตำแหน่งของ Label
        self.label.resize(860, 500)         # ปรับขนาดของ Label
        self.label.setStyleSheet("border: 1px solid black;")        # เพิ่มกรอบของ Label เพื่อกำหนดขอบเขตของพื้นที่ในการแสดงประโยคภาษาอังกฤษ และการกำกับแท็ก POS
        self.label.setFont(QFont('supermarket', 12))     # กำหนดให้ตัวหนังสือที่มีการแสดงประโยคภาษาอังกฤษ และการกำกับแท็ก POSภายใน Label ลักษณะฟ้อน ขนาดตัวหนังสือ และความหนาบางของตัวหนังสือ

        self.show()     # ให้วิดเจตต่าง ๆ ปรากฏในหน้าต่างโปรแกรม

    @pyqtSlot()     # ฟังก์ชั่น on_click
    def on_click(self):     # สร้างอ๊อบเจค on_click
        textboxValue = self.lineedit.text()     # สร้างตัวแปร textboxValue ขึ้นมาเพื่อรเก็บค่าจาก self.lineedit และปรับให้เป็นการรับค่าแบบ text โดยฟังก์ชั่น .text()

        inputs_tokens = nltk.word_tokenize(textboxValue)        # สร้างตัวแปล inputs_tokens เพื่อเก็บค่าโดยที่ไลบรารี่ nltk.word_tokenize ทำการตัดคำจาก texboxtValue ซึ่งมีการรับค่าจากอินพุท

        inputs_pos = nltk.pos_tag(inputs_tokens)        # เมื่อมีการตัดเสร็จแล้ว สร้างตัวแปล inputs_pos ขึ้นมาเพื่อเก็บค่าจากการใส่แท็ค POS โดยไลบรารี่ nltk.pos_tag
        print(inputs_pos)      # ปริ้นประโยคภาษาอังกฤษและการกำกับแท็ก POS

        # ---------------------------------------------Show type-----------------------------------------

        store = 1       # สร้างตัวแปร store เพื่อทำการเช็คเงื่อนไขในลูป while
        while (store == 1):     # คำสั่ง while loop เป็นคำสั่งวนซ้ำ ใช้ควบคุมโปรแกรมให้ทำงานซ้ำ ๆ ในขณะที่เงื่อนไขยังคงเป็นจริง และกำหนดเงื่อนไขภายใน while ให้ store มีค่าเท่ากับ 1
            for w in inputs_pos:        # คำสั่ง for loop เป็นคำสั่งวนซ้ำที่ใช้ควบคุมการทำงานซ้ำ ๆ ซึ่งย้ายค่าจากตัวแปร inputs_pos มาเก็บไว้ที่ตัวแปร w
                if (w[0] == "No"):      # กำหนดเงงื่อนไข ถ้าตัวแปร w อะเรย์ช่องที่ 1 มีค่าเท่ากับ No
                    sentence = "ประโยคปฏิเสธ"       # หากโปรแกรมตรงตามเงื่อนไขให้ตัวแปร sentence แสดงสตริง
                    store += 1      # ให้เพิ่มค่าตัวแปร store เพิ่มค่าไปอีก 1
                elif (w[0] == "Nothing"):
                    sentence = "ประโยคปฏิเสธ"
                    store += 1
                elif (w[0] == "no"):
                    sentence = "ประโยคปฏิเสธ"
                    store += 1
                elif (w[0] == "not"):
                    sentence = "ประโยคปฏิเสธ"
                    store += 1
                elif (w[1] == "WP"):
                    sentence = "ประโยคคำถาม"
                    store += 1
                elif (w[1] == "WRB"):
                    sentence = "ประโยคคำถาม"
                    store += 1
                elif (w[0] == "Are" and "you"):
                    sentence = "ประโยคคำถาม"
                    store += 1
                elif (w[0] == "Can" and "you"):
                    sentence = "ประโยคคำถาม"
                    store += 1
                elif (w[0] == "Do" and "you"):
                    sentence = "ประโยคคำถาม"
                    store += 1
                elif (store == 2):      # กำหนดเงื่อนไขถ้าตัวแปร store มีค่าเท่ากับ 2
                    break       # ถ้าโปรแกรมตรงตามเงื่อนไขให้ทำการเบรก
            else:       # ถ้าหากโปรแกรมไม่ตรงตามเงื่อนไข
                (store != 2)        # ตัวแปร store ไม่เท่ากับ 2
                sentence = "ประโยคบอกเล่า"      # ให้ตัวแปร sentence แสดงสตริง
                break       # ถ้าโปรแกรมตรงตามเงื่อนไขให้ทำการอออกจากลูป while

        # ------------------------------------------Show type------------------------------------------

        a = []      # สร้างตัวแปร a ขึ้นมาเพื่อเก็บข้อมูลเป็น list
        word3 = ""      # สร้างตัวแปร word3 เพื่อเก็บสตริง
        for w in inputs_pos:        # ลูป for ย้ายค่าจากตัวแปร inputs_pos มาเก็บไว้ที่ตัวแปร w
            if (w[1] == "CC"):      # กำหนดเงื่อนไข ถ้า w อะเรย์ ที่1 มีค่าเท่ากับ CC
                word3 = "Coordinating conjunction"      # ให้ word3 แสดงสตริง
            elif (w[1] == "CD"):
                word3 = "Cardinal digit"
            elif (w[1] == "DT"):
                word3 = "Determiner"
            elif (w[1] == "EX"):
                word3 = "existential there (like: 'there is' … think of it like 'there exists')"
            elif (w[1] == "FW"):
                word3 = "Foreign word"
            elif (w[1] == "IN"):
                word3 = "Preposition/subordinating conjunction"
            elif (w[1] == "JJ"):
                word3 = "Adjective (big)"
            elif (w[1] == "JJR"):
                word3 = "Adjective, comparative (bigger)"
            elif (w[1] == "JJS"):
                word3 = "Adjective, superlative (biggest)"
            elif (w[1] == "LS"):
                word3 = "List market"
            elif (w[1] == "MD"):
                word3 = "Modal (could, will)"
            elif (w[1] == "NN"):
                word3 = "Noun, singular (desk, cat)"
            elif (w[1] == "NNS"):
                word3 = "Noun plural (desks, cats)"
            elif (w[1] == "NNP"):
                word3 = "Proper noun, singular (sarah)"
            elif (w[1] == "NNPS"):
                word3 = "Proper noun, plural (indians or americans)"
            elif (w[1] == "PDT"):
                word3 = "Predeterminer (all, both, half)"
            elif (w[1] == "POS"):
                word3 = "Possessive ending (parent\ 's)"
            elif (w[1] == "PRP"):
                word3 = "Personal pronoun (I, he, she)"
            elif (w[1] == "PRP$"):
                word3 = "Possessive pronoun (my, his, hers)"
            elif (w[1] == "RB"):
                word3 = "Adverb (occasionally, swiftly)"
            elif (w[1] == "RBR"):
                word3 = "Adverb, comparative (greater)"
            elif (w[1] == "RBS"):
                word3 = "Adverb, superlative (biggest)"
            elif (w[1] == "RP"):
                word3 = "Particle (about)"
            elif (w[1] == "TO"):
                word3 = "Infinite marker (to)"
            elif (w[1] == "UH"):
                word3 = "Interjection (goodbye)"
            elif (w[1] == "VB"):
                word3 = "Verb (ask)"
            elif (w[1] == "VBD"):
                word3 = "Verb gerund (judging)"
            elif (w[1] == "VBG"):
                word3 = "Verb past tense (pleaded)"
            elif (w[1] == "VBN"):
                word3 = "Verb past participle (reunified)"
            elif (w[1] == "VBP"):
                word3 = "Verb, Present tense not 3rd person singular (wrap)"
            elif (w[1] == "VBZ"):
                word3 = "Verb, Present tense with 3rd person singular (bases)"
            elif (w[1] == "WDT"):
                word3 = "Wh- determiner (that, what)"
            elif (w[1] == "WP"):
                word3 = "Wh- pronoun (who, what)"
            elif (w[1] == "WP$"):
                word3 = "Possessive Wh- pronoun whose"
            elif (w[1] == "WRB"):
                word3 = "Wh- adverb (how)"

            a.append(" \n" + w[0] + " // " + w[1] + " :: " + word3)     # กำหนดให้มีการแสดงประโยคภาษาอังกฤษ แท็ก POS และความหมายของแท็กต่าง ๆ

        self.label.setText( textboxValue + "\n" + ': ' + sentence + ' '.join(a) )       # แสดงข้อความที่ได้รับจากอินพุทในตัวแปร textboxValue สตริงจากตัวแปร sentence และสตริงจากตัวแปร a โดยการเรียกใช้คำสั่ง setText


if __name__ == '__main__':      # สร้าง main ขึ้นมาเพื่อเรียกใช้งาน
    app = QApplication(sys.argv)        # สร้างแอปพลิเคชันโดยการเรียกใช้คำสั่ง QApplication และมี sys.argv เป็นอาร์กิวเมนต์
    ex = App()      # สร้างตัวแปล ex เพื่อรับค่าจากอ๊อบเจค App
    sys.exit(app.exec_())       # วนลูปโปรแกรมและส่งผ่านรหัสสถานะเมื่อโปรแกรมออกเนื่องจากพบข้อผิดพลาด