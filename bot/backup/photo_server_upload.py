import glob
import sqlite3 as sql
from mailing_db import file_finder

#создание бд
def create_photo_db():
	try:
		with sql.connect('photos.db') as con:
			cursor = con.cursor()
			cursor.execute('''CREATE TABLE IF NOT EXISTS PHOTOS(
				"photo_url" TEXT NOT NULL DEFAULT 'photo_url',
				"kurs" INTEGER NOT NULL DEFAULT 0)
				''')
			con.commit()
			cursor.close()
	except Exception as ex:
		print(f'Ошибка: {ex}')
	finally:
		if con:
			con.close()

#получение данных таблицы. Возвращает списов кортежей
def fetchall_photos():
	try:
		con = sql.connect('photos.db')
		cursor = con.cursor()
		fetchall_request = '''SELECT * from PHOTOS'''
		cursor.execute(fetchall_request)
		data = cursor.fetchall()
		con.commit()
		cursor.close()
	except Exception as ex:
		print(f'Ошибка: {ex}')
	finally:
		if con:
			con.close()
	return data

#возвращает список url'ов фото из бд
def fetch_photos():
	data = fetchall_photos()
	photos_list = []
	for record in data:
		photos_list.append(record[0])
	return photos_list

#Возвращает словарь вида {'1': [<тут url'ы фото для первого курса>], '2': [<фото для второго курса>]...}
def fetch_photo_kurs():
	data = fetchall_photos()
	kurs1 = []
	kurs2 = []
	kurs3 = []
	kurs4 = []
	for element in data:
		if element[1] == 1:
			kurs1.append(element[0])
		elif element[1] == 2:
			kurs2.append(element[0])
		elif element[1] == 3:
			kurs3.append(element[0])
		elif element[1] == 4:
			kurs4.append(element[0])
	photos_data = {
		'1': kurs1,
		'2': kurs2,
		'3': kurs3,
		'4': kurs4
	}
	return photos_data

#загрузка фото в бд
def upload_photo(photos, kurs_number):
	try:
		con = sql.connect('photos.db')
		cursor = con.cursor()
		upload_request = '''INSERT INTO PHOTOS ("photo_url", "kurs") VALUES (?, ?)'''
		kurs = kurs_number
		photos_in_db = fetch_photos()
		for photo in photos:
			if photo not in photos_in_db:
				data = (photo, kurs_number)
				cursor.execute(upload_request, data)
				con.commit()
				print(f'фото: {photo}, курс: {kurs_number}.')
			else:
				print(f'Фото: {photo} уже есть в бд')
		cursor.close()
	except Exception as ex:
		print(f'Ошибка: {ex}')
	finally:
		if con:
			con.close()

def delete_photos():
	try:
		con = sql.connect('photos.db')
		cursor = con.cursor()
		delete_old_photos = '''DELETE FROM PHOTOS where kurs = ?'''
		attachment = [(1,), (2,), (3,), (4,)]
		cursor.executemany(delete_old_photos, attachment)
		con.commit()
	except Exception as ex:
		print(f'Ошибка: {ex}')
	finally:
		if con:
			con.close()

#@bot.on.message(text = '/photos')
#async def photo_upload(message: Message):
#	#получаю id пользователя
#	user = await bot.api.users.get(message.from_id)
#	user_id = user[0].id
#	if user_id == 188529333 or user_id == 461222890:
#		kurs1 = file_finder(1, 'C:\\Users\\Vladik\\Downloads\\photo_files\\*')
#		kurs2 = file_finder(2, 'C:\\Users\\Vladik\\Downloads\\photo_files\\*')
#		kurs3 = file_finder(3, 'C:\\Users\\Vladik\\Downloads\\photo_files\\*')
#		kurs4 = file_finder(4, 'C:\\Users\\Vladik\\Downloads\\photo_files\\*')
#		#kurs1 = file_finder(1, '\\home\\kravasos\\new_vk_bot\\photo_files\\*')
#		#kurs2 = file_finder(2, '\\home\\kravasos\\new_vk_bot\\photo_files\\*')
#		#kurs3 = file_finder(3, '\\home\\kravasos\\new_vk_bot\\photo_files\\*')
#		#kurs4 = file_finder(4, '\\home\\kravasos\\new_vk_bot\\photo_files\\*')
#		kurses = [kurs1, kurs2, kurs3, kurs4]
#		print('\n\n\n')
#		print(kurses)
#		print('\n\n\n')
#		kurs_dict = {}
#		photos = []
#		delete_photos()
#		for kurs in kurses:
#			try:
#				kurs_number = kurses.index(kurs) + 1
#				for i in range(len(kurs)):
#					kurs_dict[i] = await photo_upd.upload(f'{kurs[i]}')
#				for i in range(len(kurs)):	
#					photos.append(kurs_dict[i])
#				upload_photo(photos, kurs_number)
#				await message.answer(f'Фото для курса {kurs_number} загружены на сервер.')
#			except Exception as ex:
#				print(f'Ошибка: {ex}')
#	else:
#		await message.answer('У вас нет доступа к этой команде')#