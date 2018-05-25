from diss.wsgi import application
from schedule_editor import models
import xml.etree.ElementTree as ET


tree = ET.parse('D:\\Education\\Диссертация\\РУП\\020302_17-1ФИИТ.plm.xml')
root = tree.getroot()

'''Группа'''
group = tree.find('.//Титул')
form = tree.find('.//План')
qualification = tree.find('.//Квалификация')
new_group = models.StudentGroup()
new_group.name = group.get('ИмяПлана')
new_group.year = group.get('ГодНачалаПодготовки')
if (qualification.get('Название') == 'бакалавр'):
    new_group.qualification = 'BAC'
elif (qualification.get('Название') == 'магистрант'):
    new_group.qualification = 'MAG'
elif (qualification.get('Название') == 'специалист'):
    new_group.qualification = 'SPC'

if (form.get('ФормаОбучения') == 'очная'):
    new_group.form = 'OC'
elif (form.get('ФормаОбучения') == 'заочная'):
    new_group.form = 'ZA'
new_group.save()

'''Семестр'''
graphic = tree.find('.//ГрафикУчПроцесса')
curse_count = 1
all_disciplines = tree.findall('.//СтрокиПлана//Строка')

for curse in graphic.findall('.//Курс'):
    sem_count = 1
    if 'КаникулНед' not in curse.attrib:
        print("curse")
        continue
    for sem in curse.findall('.//Семестр'):
        # new_semester = models.Semester()
        if (int(sem.get('Ном')) == sem_count):
            new_semester = models.Semester()
            new_semester.student_group = new_group
            new_semester.year = int(group.get('ГодНачалаПодготовки')) + (curse_count - 1) + (sem_count - 1)
            new_semester.semester = models.Semester.SEMESTER[sem_count - 1][0]
            new_semester.save()
            '''Дисциплины'''
            for discipline in all_disciplines:
                for sem_d in discipline.findall('.//Сем'):
                    if (int(sem.get('Ном'))-1 == (int(sem_d.get('Ном'))+1)%2 and int(sem_d.get('Ном')) == curse_count * 2 - sem_count % 2):
                        new_subject = models.Subject()
                        new_subject.name = discipline.get('Дис')
                        new_subject.semester = new_semester
                        new_subject.save()
            sem_count += 1
    curse_count += 1




# new_subject = models.Subject()
# new_subject.name = "ыапыва"
# new_subject.semester = models.Semester.objects.get(id=1)
#
# new_subject.save()


# Вывод списка дисциплин
# for child in root:
# 	for child2 in child:
# 		for child3 in child2:
# 			if (child3.get('Дис') != None):
# 				print(child3.get('Дис'))
#
# // Поиск всех тегов с именем "Строка"
#
# all_string = tree.findall('.//Строка')
#
# // Вывод списка дисциплин
# all_string = tree.findall('.//СтрокиПлана//Строка')
# for f in all_string:
# 	print (f.get('Дис')
#
# //........
# for f in all_string:
# 	sem = f.findall('.//Сем')
# 	print(f.get('Дис'))
# 	for s in sem:
# 		print("Лек", s.get('Лек'), "	Пр", s.get('Пр'), "	КСР", s.get('КСР'), "	СРС", s.get('СРС'), "ЗЕТ", s.get('ЗЕТ'))

