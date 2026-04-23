import sys
from PyQt6.QtWidgets import (QApplication, QWidget, QVBoxLayout, 
                             QLabel, QLineEdit, QPushButton, QMessageBox)
from PyQt6.QtCore import Qt

class SurveyApp(QWidget):
    def __init__(self):
        super().__init__()
        # Список питань (усього 8)
        self.questions = [
            "Ваше ім'я:",
            "Ваш вік:",
            "Яке ваше улюблене хобі?",
            "Яка ваша найбільша мета на цей рік?",
            "Що для вас є найкращим відпочинком?",
            "Яку останню книгу ви прочитали або фільм подивилися?",
            "Ваша улюблена пора року та чому?",
            "Яку пораду ви б дали собі 5 років тому?"
        ]
        self.current_index = 0
        self.answers = [] # Тимчасове сховище для поточної сесії
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Опитування про життя')
        self.setGeometry(300, 300, 450, 250)

        self.layout = QVBoxLayout()

        # Номер питання та текст
        self.step_label = QLabel(f"Питання {self.current_index + 1} з {len(self.questions)}")
        self.step_label.setStyleSheet("color: gray; font-size: 11px;")
        
        self.question_label = QLabel(self.questions[self.current_index])
        self.question_label.setStyleSheet("font-size: 15px; font-weight: bold; margin-bottom: 10px;")
        self.question_label.setWordWrap(True)

        # Поле для відповіді
        self.answer_input = QLineEdit()
        self.answer_input.setPlaceholderText('Введіть відповідь...')
        self.answer_input.returnPressed.connect(self.handle_next) # Перехід по Enter

        # Кнопка
        self.next_btn = QPushButton('Далі')
        self.next_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.next_btn.setMinimumHeight(40)
        self.next_btn.clicked.connect(self.handle_next)

        self.layout.addWidget(self.step_label)
        self.layout.addWidget(self.question_label)
        self.layout.addWidget(self.answer_input)
        self.layout.addSpacing(20)
        self.layout.addWidget(self.next_btn)

        self.setLayout(self.layout)

    def handle_next(self):
        answer = self.answer_input.text().strip()

        if not answer:
            QMessageBox.warning(self, 'Увага', 'Будь ласка, введіть відповідь!')
            return

        # Додаємо відповідь у список
        self.answers.append(f"{self.questions[self.current_index]} {answer}")
        
        self.current_index += 1

        if self.current_index < len(self.questions):
            # Оновлюємо інтерфейс для наступного питання
            self.step_label.setText(f"Питання {self.current_index + 1} з {len(self.questions)}")
            self.question_label.setText(self.questions[self.current_index])
            self.answer_input.clear()
            
            if self.current_index == len(self.questions) - 1:
                self.next_btn.setText('Завершити')
        else:
            self.save_to_file()

    def save_to_file(self):
        try:
            with open('survey_results.txt', 'a', encoding='utf-8') as f:
                f.write("--- Нова анкета ---\n")
                for item in self.answers:
                    f.write(f"{item}\n")
                f.write("\n")
            
            QMessageBox.information(self, 'Готово', 'Дякуємо! Всі ваші відповіді збережені у файл survey_results.txt')
            self.close() # Закриваємо застосунок після завершення
            
        except Exception as e:
            QMessageBox.critical(self, 'Помилка', f'Не вдалося зберегти дані: {e}')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    # Встановлення стилю для кращого вигляду (опціонально)
    app.setStyle('Fusion') 
    ex = SurveyApp()
    ex.show()
    sys.exit(app.exec())