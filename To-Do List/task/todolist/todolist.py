from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date
from datetime import datetime, timedelta
from sqlalchemy.orm import sessionmaker


engine = create_engine('sqlite:///todo.db?check_same_thread=False')
Base = declarative_base()


class Task(Base):
    __tablename__ = 'task'
    id = Column(Integer, primary_key=True)
    task = Column(String, default='default_value')
    deadline = Column(Date, default=datetime.today())

    def __repr__(self):
        return self.string_field

Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()
today = datetime.today()

# Write your code here
while True:
    start_menu = int(input(
        "1) Today's tasks\n"
        "2) Week's tasks\n"
        "3) All tasks\n"
        "4) Missed tasks\n"
        "5) Add task\n"
        "6) Delete task\n"
        "0) Exit\n"
    ))
    if start_menu == 0:
        break

    elif start_menu == 1:
        today_list = session.query(Task).filter(Task.deadline == today.date()).all()
        if not today_list:
            print("Nothing to do!")
        else:
            print(f"\nToday {today.strftime('%d %b')}:")
            for item in today_list:
                print(item.task)
        print()

    elif start_menu == 2:
        for day in range(7):
            print(f'{(today + timedelta(days=day)).strftime("%A %d %b")}:')
            week_day_list = session.query(Task).filter(Task.deadline == (today + timedelta(days=day)).date()).all()
            if not week_day_list:
                print("Nothing to do!")
            else:
                for item in week_day_list:
                    print(f'{item.id}. {item.task}')
            print()

    elif start_menu == 3:
        all_tasks = session.query(Task).order_by(Task.deadline).all()
        print('\nAll tasks:')
        if not all_tasks:
            print("Nothing to do!")
        else:
            item_number = 0
            for item in all_tasks:
                item_number += 1
                print(f'{item_number}. {item.task}. {item.deadline.strftime("%d %b")}')
            print()

    elif start_menu == 4:
        missed_tasks = session.query(Task).filter(Task.deadline < today.date()).order_by(Task.deadline).all()
        print('\nAll tasks:')
        if not missed_tasks:
            print("Nothing is missed!")
        else:
            item_number = 0
            for item in missed_tasks:
                item_number += 1
                print(f'{item_number}. {item.task}. {item.deadline.strftime("%d %b")}')
            print()

    elif start_menu == 5:
        new_row = Task(task=input("\nEnter task"),
                       deadline=datetime.strptime(input("\nEnter deadline"), "%Y-%m-%d")
                       )
        session.add(new_row)
        session.commit()
        print("The task has been added!\n")

    elif start_menu == 6:
        delete_tasks = session.query(Task).order_by(Task.deadline).all()
        item_number = 0
        for item in delete_tasks:
            item_number += 1
            print(f'{item_number}. {item.task}. {item.deadline.strftime("%d %b")}')
        print()
        delete_row = delete_tasks[int(input('\nChoose the number of task you want to delete:')) - 1]
        session.delete(delete_row)
        session.commit()
        print("The task has been deleted!\n")

print("\nBye!")

