/**
 *  author:   Yuriy Lobarev
 *  telegram: @forman
 *  phone:    +7(910)983-95-90
 *  email:    forman@anyks.com
 *  site:     https://anyks.com
 */

#ifndef _ANYKS_LM_
#define _ANYKS_LM_

/**
 * Системные модули
 */
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include <pybind11/complex.h>
#include <pybind11/pybind11.h>
#include <pybind11/functional.h>
/**
 * Наши модули
 */
#include <alm.hpp>
#include <ablm.hpp>

// Устанавливаем область видимости
using namespace std;
// Устанавливаем область видимости
namespace py = pybind11;
// Устанавливаем конвертер типов данных
template <typename... Args>
using overload_cast_ = py::detail::overload_cast_impl <Args...>;
/**
 * anyks пространство имён
 */
namespace anyks {
	// Флаги удаления в слове
	enum class wdel_t : u_short {
		punct,  // Флаг удаления знаков пунктуации в слове
		broken, // Флаг удаления плохих слов в слове
		hyphen  // Флаг удаления дефисов в слове
	};
	// Флаги очистики
	enum class clear_t : u_short {
		all,      // Флаг полной очистки
		utokens,  // Флаг очистки пользовательских токенов
		badwords, // Флаг очистки чёрного списка
		goodwords // Флаг очистки белого списка
	};
	// Флаги проверки
	enum class check_t : u_short {
		home2,   // Флаг проверки слова по типу Дом-2
		latian,  // Флаг проверки на наличие латинского символа
		hyphen,  // Флаг проверки на наличие доефиса
		letter,  // Флаг проверки легальности буквы
		similars // Флаг проверки смешанных букв разных словарей
	};
	// Основные опции
	enum class options_t : u_short {
		debug,     // Флаг режима отладки
		stress,    // Флаг разрешения использовать символы ударения
		uppers,    // Флаг разрешения проставлять регистры букв в словах
		collect,   // Флаг разрешения сборку суффиксов цифровых аббревиатур
		onlyGood,  // Флаг использования только слов из белого списка
		mixdicts,  // Флаг разрешающий детектировать слова из смешанных словарей
		confidence // Флаг разрешающий загружать n-граммы из arpa так-как они есть
	};
	// Флаги соответствия
	enum class match_t : u_int {
		url,      // Флаг проверки соответствия слова url адресу
		abbr,     // Флаг проверки на соответствие слова аббревиатуре
		math,     // Флаг определения математических операий
		upper,    // Флаг проверки символ на верхний регистр
		punct,    // Флаг проверки является ли буква, знаком препинания
		space,    // Флаг проверки является ли буква, пробелом
		latian,   // Флаг проверки является ли строка латиницей
		number,   // Флаг проверки является ли слово числом
		anumber,  // Флаг проверки является ли косвенно слово числом
		allowed,  // Флаг проверки соответствия слова словарю
		decimal,  // Флаг проверки является ли слово дробным числом
		special,  // Флаг определения спец-символа
		isolation // Флаг определения знака изоляции (кавычки, скобки)
	};
	// Адрес лог файла
	string logfile = "";
	// Создаём объект алфавита
	alphabet_t alphabet;
	// Создаём объект токенизатора
	tokenizer_t tokenizer(&alphabet);
	// Создаём обхъект языковой модели
	unique_ptr <alm_t> alm(new alm1_t(&alphabet, &tokenizer));
	/**
	 * Methods Основные методы библиотеки
	 */
	namespace Methods {
		/**
		 * allowStress Метод разрешения, использовать ударение в словах
		 */
		void allowStress() noexcept {
			// Разрешаем использовать ударение в словах
			tokenizer.setOption(tokenizer_t::options_t::stress);
		}
		/**
		 * disallowStress Метод запрещения использовать ударение в словах
		 */
		void disallowStress() noexcept {
			// Запрещаем использовать ударение в словах
			tokenizer.unsetOption(tokenizer_t::options_t::stress);
		}
		/**
		 * idt Метод извлечения идентификатора токена
		 * @param  word слово для получения идентификатора
		 * @return      идентификатор токена
		 */
		const size_t idt(const wstring & word) noexcept {
			// Выводим идентификатор токена
			return size_t(tokenizer.idt(word));
		}
		/**
		 * setZone Метод установки пользовательской зоны
		 * @param zone пользовательская зона
		 */
		void setZone(const wstring & zone) noexcept {
			// Устанавливаем доменную зону
			alphabet.setzone(zone);
		}
		/**
		 * addAbbr Метод добавления аббревиатуры
		 * @param idw идентификатор слова для добавления
		 */
		void addAbbr(const size_t idw) noexcept {
			// Добавляем аббревиатуру
			tokenizer.addAbbr(idw);
		}
		/**
		 * addAbbr Метод добавления аббревиатуры
		 * @param word слово для добавления
		 */
		void addAbbr(const wstring & word) noexcept {
			// Добавляем аббревиатуру
			tokenizer.addAbbr(word);
		}
		/**
		 * setAbbrs Метод установки списка аббревиатур
		 * @param abbrs список аббревиатур
		 */
		void setAbbrs(const set <size_t> & abbrs) noexcept {
			// Устанавливаем список аббревиатур
			tokenizer.setAbbrs(abbrs);
		}
		/**
		 * addSuffix Метод установки суффикса цифровой аббревиатуры
		 * @param idw идентификатор суффикса цифровой аббревиатуры
		 */
		void addSuffix(const size_t idw) noexcept {
			// Устанавливаем идентификатор суффикса цифровой аббревиатуры
			tokenizer.addSuffix(idw);
		}
		/**
		 * setSuffixes Метод установки списка суффиксов цифровых аббревиатур
		 * @param suffix список суффиксов цифровых аббревиатур
		 */
		void setSuffixes(const set <size_t> & suffix) noexcept {
			// Устанавливаем список суффиксов цифровых аббревиатур
			tokenizer.setSuffixes(suffix);
		}
		/**
		 * addSuffix Метод извлечения суффикса из цифровой аббревиатуры
		 * @param word слово для извлечения суффикса аббревиатуры
		 * @param idw  идентификатор обрабатываемого слова
		 */
		void addSuffix(const wstring & word, const size_t idw = idw_t::NIDW) noexcept {
			// Устанавливаем суффикс цифровой аббревиатуры
			tokenizer.addSuffix(word, idw);
		}
		/**
		 * setAlphabet Метод установки алфавита
		 * @param text алфавит символов для текущего языка
		 */
		void setAlphabet(const wstring & text) noexcept {
			// Устанавливаем алфавит
			alphabet.set(alphabet.convert(text));
			// Обновляем токенайзер
			tokenizer.update();
		}
		/**
		 * setUnknown Метод установки неизвестного слова
		 * @param word слово для добавления
		 */
		void setUnknown(const wstring & word) noexcept {
			// Выполняем установку неизвестного слова
			alm->setUnknown(alphabet.convert(word));
		}
		/**
		 * getName Метод извлечения названия библиотеки
		 * @return название библиотеки
		 */
		const wstring getName() noexcept {
			// Выводим результат
			return alphabet.convert(ANYKS_LM_NAME);
		}
		/**
		 * sentences Метод генерации предложений
		 * @param callback функция обратного вызова
		 */
		void sentences(function <const bool (const wstring &)> callback) noexcept {
			// Выполняем генерацию предложений
			alm->sentences(callback);
		}
		/**
		 * getEmail Метод извлечения электронной почты автора
		 * @return электронная почта автора
		 */
		const wstring getEmail() noexcept {
			// Выводим результат
			return alphabet.convert(ANYKS_LM_EMAIL);
		}
		/**
		 * getPhone Метод извлечения телефона автора
		 * @return номер телефона автора
		 */
		const wstring getPhone() noexcept {
			// Выводим результат
			return alphabet.convert(ANYKS_LM_PHONE);
		}
		/**
		 * getAuthor Метод извлечения имени автора
		 * @return имя автора библиотеки
		 */
		const wstring getAuthor() noexcept {
			// Выводим результат
			return alphabet.convert(ANYKS_LM_AUTHOR);
		}
		/**
		 * findNgram Метод поиска n-грамм в тексте
		 * @param text     текст в котором необходимо найти n-граммы
		 * @param callback функция обратного вызова
		 */
		void findNgram(const wstring & text, function <void (const wstring &)> callback) noexcept {
			// Выполняем поиск n-грамм в тексте
			alm->find(text, callback);
		}
		/**
		 * setOption Метод установки опций модуля
		 * @param option опция для установки
		 */
		void setOption(const options_t option) noexcept {
			// Устанавливаем нужный нам тип настроек
			switch((u_short) option){
				// Если включён режим отладки
				case (u_short) options_t::debug: {
					// Выполняем установку опций модуля
					alm->setOption(alm_t::options_t::debug);
					// Устанавливаем режим отладки для токенизатора
					tokenizer.setOption(tokenizer_t::options_t::debug);
				} break;
				// Устанавливаем флаг использования только слов из белого списка
				case (u_short) options_t::onlyGood: alm->setOption(alm_t::options_t::onlyGood); break;
				// Устанавливаем флаг разрешающий детектировать слова из смешанных словарей
				case (u_short) options_t::mixdicts: alm->setOption(alm_t::options_t::mixdicts); break;
				// Устанавливаем флаг разрешающий загружать n-граммы из arpa так-как они есть
				case (u_short) options_t::confidence: alm->setOption(alm_t::options_t::confidence); break;
				// Устанавливаем флаг разрешения использовать символы ударения
				case (u_short) options_t::stress: tokenizer.setOption(tokenizer_t::options_t::stress); break;
				// Устанавливаем флаг разрешения проставлять регистры букв в словах
				case (u_short) options_t::uppers: tokenizer.setOption(tokenizer_t::options_t::uppers); break;
				// Устанавливаем флаг разрешения сборку суффиксов цифровых аббревиатур
				case (u_short) options_t::collect: tokenizer.setOption(tokenizer_t::options_t::collect); break;
			}
		}
		/**
		 * getUnknown Метод извлечения неизвестного слова
		 * @return установленное неизвестное слово
		 */
		const wstring getUnknown() noexcept {
			// Выводим результат
			return alphabet.convert(alm->getUnknown());
		}
		/**
		 * size Метод получения размера n-грамы
		 * @return длина n-граммы в языковой моделе
		 */
		const size_t size() noexcept {
			// Выводим результат
			return alm->getSize();
		}
		/**
		 * jsonToText Метод преобразования текста в формате json в текст
		 * @param text     текст для преобразования в формате json
		 * @param callback функция обратного вызова
		 */
		void jsonToText(const wstring & text, function <void (const wstring &)> callback) noexcept {
			// Запускаем обработку конвертации
			tokenizer.jsonToText(alphabet.convert(text), [&callback](const string & chunk){
				// Выводим результат
				callback(alphabet.convert(chunk));
			});
		}
		/**
		 * textToJson Метод преобразования текста в json
		 * @param text     текст для преобразования
		 * @param callback функция обратного вызова
		 */
		void textToJson(const wstring & text, function <void (const wstring &)> callback) noexcept {
			// Запускаем обработку конвертации
			tokenizer.textToJson(alphabet.convert(text), [&callback](const string & chunk){
				// Выводим результат
				callback(alphabet.convert(chunk));
			});
		}
		/**
		 * restore Метод восстановления текста из контекста
		 * @param context токенизированный контекст
		 * @return        результирующий текст
		 */
		const wstring restore(const vector <wstring> & context) noexcept {
			// Восстанавливаем текст
			return tokenizer.restore(context);
		}
		/**
		 * unsetOption Метод отключения опции модуля
		 * @param option опция для отключения
		 */
		void unsetOption(const options_t option) noexcept {
			// Выполняем отключение нужный нам тип настроек
			switch((u_short) option){
				// Если включён режим отладки
				case (u_short) options_t::debug: {
					// Выполняем установку опций модуля
					alm->unsetOption(alm_t::options_t::debug);
					// Выполняем отключение режим отладки для токенизатора
					tokenizer.unsetOption(tokenizer_t::options_t::debug);
				} break;
				// Выполняем отключение флаг использования только слов из белого списка
				case (u_short) options_t::onlyGood: alm->unsetOption(alm_t::options_t::onlyGood); break;
				// Выполняем отключение флаг разрешающий детектировать слова из смешанных словарей
				case (u_short) options_t::mixdicts: alm->unsetOption(alm_t::options_t::mixdicts); break;
				// Выполняем отключение флаг разрешающий загружать n-граммы из arpa так-как они есть
				case (u_short) options_t::confidence: alm->unsetOption(alm_t::options_t::confidence); break;
				// Выполняем отключение флаг разрешения использовать символы ударения
				case (u_short) options_t::stress: tokenizer.unsetOption(tokenizer_t::options_t::stress); break;
				// Выполняем отключение флаг разрешения проставлять регистры букв в словах
				case (u_short) options_t::uppers: tokenizer.unsetOption(tokenizer_t::options_t::uppers); break;
				// Выполняем отключение флаг разрешения сборку суффиксов цифровых аббревиатур
				case (u_short) options_t::collect: tokenizer.unsetOption(tokenizer_t::options_t::collect); break;
			}
		}
		/**
		 * getBadwords Метод извлечения чёрного списка
		 * @return чёрный список слов
		 */
		const set <size_t> & getBadwords() noexcept {
			// Выводим результат
			return alm->getBadwords();
		}
		/**
		 * setUserToken Метод добавления токена пользователя
		 * @param name слово - обозначение токена
		 */
		void setUserToken(const wstring & name) noexcept {
			// Выполняем добавление токена пользователя
			alm->setUserToken(alphabet.convert(name));
		}
		/**
		 * getGoodwords Метод извлечения белого списка
		 * @return белый список слов
		 */
		const set <size_t> & getGoodwords() noexcept {
			// Выводим результат
			return alm->getGoodwords();
		}
		/**
		 * setLogfile Метод установки файла для вывода логов
		 * @param file адрес файла для вывода отладочной информации
		 */
		void setLogfile(const wstring & file) noexcept {
			// Если адрес логов передан
			if(!file.empty()){
				// Запоминаем адрес файла логов
				logfile = alphabet.convert(file);
				// Выполняем установку файла для вывода логов
				alm->setLogfile(logfile.c_str());
			}
		}
		/**
		 * setOOvFile Метод установки файла для сохранения OOV слов
		 * @param oovfile адрес файла для сохранения oov слов
		 */
		void setOOvFile(const wstring & oovfile) noexcept {
			// Выполняем установку файла для сохранения OOV слов
			if(!oovfile.empty()) alm->setOOvFile(alphabet.convert(oovfile).c_str());
		}
		/**
		 * pplConcatenate Метод объединения перплексий
		 * @param ppl1 первая перплексия
		 * @param ppl2 вторая перплексия
		 * @return     объединённая перплексия
		 */
		const alm_t::ppl_t pplConcatenate(const alm_t::ppl_t & ppl1, const alm_t::ppl_t & ppl2) noexcept {
			// Выполняем расчёт перплексии
			return alm->pplConcatenate(ppl1, ppl2);
		}
		/**
		 * getUserTokens Метод извлечения списка пользовательских токенов
		 * @return список пользовательских токенов
		 */
		const vector <wstring> getUserTokens() noexcept {
			// Результат работы функции
			vector <wstring> result;
			// Получаем список токенов
			const auto & tokens = alm->getUserTokens();
			// Если токены получены
			if(!tokens.empty()){
				// Переходим по списку токенов
				for(auto & token : tokens) result.push_back(alphabet.convert(token));
			}
			// Выводим результат
			return result;
		}
		/**
		 * tokenization Метод разбивки текста на токены
		 * @param text     входной текст для обработки
		 * @param callback функция обратного вызова
		 */
		void tokenization(const wstring & text, function <const bool (const wstring &, const vector <wstring> &, const bool, const bool)> callback) noexcept {
			// Контекст сконвертированный
			vector <wstring> seq;
			// Запускаем обработку токенизации
			tokenizer.run(text, [&seq, &callback](const wstring & word, const vector <string> & context, const bool reset, const bool stop){
				// Очищаем список последовательности
				seq.clear();
				// Если последовательность получена
				if(!context.empty()){
					// Переходим по всему контексту
					for(auto & word : context) seq.push_back(alphabet.convert(word));
				}
				// Выводим результат
				return callback(word, seq, reset, stop);
			});
		}
		/**
		 * fixUppers Метод исправления регистров в тексте
		 * @param text текст для исправления регистров
		 * @return     текст с исправленными регистрами слов
		 */
		const wstring fixUppers(const wstring & text) noexcept {
			// Выполняем исправление регистров в тексте
			return alm->fixUppers(text);
		}
		/**
		 * checkHypLat Метод поиска дефиса и латинского символа
		 * @param str строка для проверки
		 * @return    результат проверки
		 */
		const pair <bool, bool> checkHypLat(const wstring & str) noexcept {
			// Выводим результат првоерки
			return alphabet.checkHypLat(str);
		}
		/**
		 * getContact Метод извлечения контактных данных автора
		 * @return контактные данные автора
		 */
		const wstring getContact() noexcept {
			// Выводим результат
			return alphabet.convert(ANYKS_LM_CONTACT);
		}
		/**
		 * getUppers Метод извлечения регистров для каждого слова
		 * @param seq последовательность слов для сборки контекста
		 * @return    список извлечённых последовательностей
		 */
		const vector <size_t> getUppers(const vector <size_t> & seq) noexcept {
			// Создаём список регистров
			vector <size_t> upps;
			// Выполняем извлечение регистров для каждого слова
			alm->getUppers(seq, upps);
			// Выводим список регистров
			return upps;
		}
		/**
		 * getSite Метод извлечения адреса сайта автора
		 * @return адрес сайта автора
		 */
		const wstring getSite() noexcept {
			// Выводим результат
			return alphabet.convert(ANYKS_LM_SITE);
		}
		/**
		 * getAlphabet Метод получения алфавита языка
		 * @return алфавит языка
		 */
		const wstring getAlphabet() noexcept {
			// Выводим данные алфавита
			return alphabet.convert(alphabet.get());
		}
		/**
		 * urls Метод извлечения координат url адресов в строке
		 * @param text текст для извлечения url адресов
		 * @return     список координат с url адресами
		 */
		const map <size_t, size_t> urls(const wstring & text) noexcept {
			// Выводим координаты url адреса
			return alphabet.urls(text);
		}
		/**
		 * getVersion Метод получения версии языковой модели
		 * @return версия языковой модели
		 */
		const wstring getVersion() noexcept {
			// Выводим результат
			return alphabet.convert(ANYKS_LM_VERSION);
		}
		/**
		 * isAllowApostrophe Метод проверки разрешения апострофа
		 * @return результат проверки
		 */
		const bool isAllowApostrophe() noexcept {
			// Выводрим результат проверки
			return alphabet.isAllowApostrophe();
		}
		/**
		 * isToken Метод проверки идентификатора на токен
		 * @param idw идентификатор слова для проверки
		 * @return    результат проверки
		 */
		const bool isToken(const size_t idw) noexcept {
			// Выполняем проверку на токен
			return tokenizer.isToken(idw);
		}
		/**
		 * isIdWord Метод проверки на соответствие идентификатора слову
		 * @param idw идентификатор слова для проверки
		 * @return    результат проверки идентификатора
		 */
		const bool isIdWord(const size_t idw) noexcept {
			// Выполняем проверку на соответствие токена разрешённому слову
			return tokenizer.isIdWord(idw);
		}
		/**
		 * isAbbr Метод проверки слова на соответствие аббревиатуры
		 * @param idw идентификатор слова для проверки
		 * @return    результат проверки
		 */
		const bool isAbbr(const size_t idw) noexcept {
			// Выводим результат проверки на аббревиатуру
			return tokenizer.isAbbr(idw);
		}
		/**
		 * isAbbr Метод проверки слова на соответствие аббревиатуры
		 * @param  word слово для проверки
		 * @return      результат проверки
		 */
		const bool isAbbr(const wstring & word) noexcept {
			// Выводим результат проверки на аббревиатуру
			return tokenizer.isAbbr(word);
		}
		/**
		 * isSuffix Метод проверки слова на суффикс цифровой аббревиатуры
		 * @param  word слово для проверки
		 * @return      результат проверки
		 */
		const bool isSuffix(const wstring & word) noexcept {
			// Выводим результат проверки на суффикс цифровой аббревиатуры
			return tokenizer.isSuffix(word);
		}
		/**
		 * getUserTokenId Метод получения идентификатора пользовательского токена
		 * @param name слово для которого нужно получить идентификатор
		 * @return     идентификатор пользовательского токена соответствующий слову
		 */
		const size_t getUserTokenId(const wstring & name) noexcept {
			// Выводим результат
			return alm->getUserTokenId(alphabet.convert(name));
		}
		/**
		 * roman2Arabic Метод перевода римских цифр в арабские
		 * @param  word римское число
		 * @return      арабское число
		 */
		const size_t roman2Arabic(const wstring & word) noexcept {
			// Выводим конвертацию чисел
			return alphabet.roman2Arabic(alphabet.toLower(word));
		}
		/**
		 * rest Метод исправления и детектирования слов со смешанными алфавитами
		 * @param  word слово для проверки и исправления
		 * @return      результат исправления
		 */
		const wstring rest(const wstring & word) noexcept {
			// Создаем слово для исправления
			wstring result = alphabet.toLower(word);
			// Выполняем исправление слов
			alphabet.rest(result);
			// Выводим результат
			return result;
		}
		/**
		 * setTokensDisable Метод установки списка запрещённых токенов
		 * @param tokens список токенов для установки
		 */
		void setTokensDisable(const set <size_t> & tokens) noexcept {
			// Если токены переданы
			if(!tokens.empty()){
				// Сприсок токенов
				set <token_t> tmp;
				// Переходим по всему списку токенов
				for(auto & token : tokens) tmp.emplace(token_t(token));
				// Выполняем установку списка запрещённых токенов
				alm->setTokensDisable(tmp);
			}
		}
		/**
		 * setTokenDisable Метод установки списка не идентифицируемых токенов
		 * @param options список не идентифицируемых токенов
		 */
		void setTokenDisable(const wstring & options) noexcept {
			// Выполняем установку списка не идентифицируемых токенов
			alm->setTokenDisable(alphabet.convert(options));
		}
		/**
		 * setAllTokenDisable Метод установки всех токенов как не идентифицируемых
		 */
		void setAllTokenDisable() noexcept {
			// Выполняем установку всех токенов как не идентифицируемых
			alm->setAllTokenDisable();
		}
		/**
		 * setTokensUnknown Метод установки списка токенов приводимых к <unk>
		 * @param tokens список токенов для установки
		 */
		void setTokensUnknown(const set <size_t> & tokens) noexcept {
			// Если токены переданы
			if(!tokens.empty()){
				// Сприсок токенов
				set <token_t> tmp;
				// Переходим по всему списку токенов
				for(auto & token : tokens) tmp.emplace(token_t(token));
				// Выполняем установку списка токенов приводимых к <unk>
				alm->setTokensUnknown(tmp);
			}
		}
		/**
		 * getTokensDisable Метод извлечения списка запрещённых токенов
		 * @return список токенов
		 */
		const set <size_t> getTokensDisable() noexcept {
			// Результат работы функции
			set <size_t> result;
			// Извлекаем список токенов
			const auto & tokens = alm->getTokensDisable();
			// Если список токенов получен
			if(!tokens.empty()){
				// Переходим по всему списку токенов
				for(auto & token : tokens) result.emplace(size_t(token));
			}
			// Выводим результат
			return result;
		}
		/**
		 * countLetter Метод подсчета количества указанной буквы в слове
		 * @param word   слово в котором нужно подсчитать букву
		 * @param letter букву которую нужно подсчитать
		 * @return       результат подсчёта
		 */
		const size_t countLetter(const wstring & word, const wstring & letter) noexcept {
			// Выводим результат подсчёта
			return alphabet.countLetter(word, letter.front());
		}
		/**
		 * setAllTokenUnknown Метод установки всех токенов идентифицируемых как <unk>
		 */
		void setAllTokenUnknown() noexcept {
			// Выполняем установку всех токенов идентифицируемых как <unk>
			alm->setAllTokenUnknown();
		}
		/**
		 * countAlphabet Метод получения количества букв в словаре
		 * @return количество букв в словаре
		 */
		const size_t countAlphabet() noexcept {
			// Выводим количество букв в словаре
			return alphabet.count();
		}
		/**
		 * getUserTokenWord Метод получения пользовательского токена по его идентификатору
		 * @param idw идентификатор пользовательского токена
		 * @return    пользовательский токен соответствующий идентификатору
		 */
		const wstring getUserTokenWord(const size_t idw) noexcept {
			// Выводим результат
			return alphabet.convert(alm->getUserTokenWord(idw));
		}
		/**
		 * setWordPreprocessingMethod Метод установки функции препроцессинга слова
		 * @param fn внешняя функция препроцессинга слова
		 */
		void setWordPreprocessingMethod(function <const string (const string &, const vector <string> &)> fn) noexcept {
			// Устанавливаем функцию
			alm->setWordPreprocessingMethod(fn);
		}
		/**
		 * setUserTokenMethod Метод установки функции обработки пользовательского токена
		 * @param name слово - обозначение токена
		 * @param fn   внешняя функция обрабатывающая пользовательский токен
		 */
		void setUserTokenMethod(const wstring & name, function <const bool (const string &, const string &)> fn) noexcept {
			// Выполняем добавление функции обработки пользовательского токена
			alm->setUserTokenMethod(alphabet.convert(name), fn);
		}
		/**
		 * setSubstitutes Метод установки букв для исправления слов из смешанных алфавитов
		 * @param letters список букв разных алфавитов соответствующих друг-другу
		 */
		void setSubstitutes(const map <wstring, wstring> & letters) noexcept {
			// Если список букв получен
			if(!letters.empty()){
				// Создаём список букв
				map <string, string> tmp;
				// Переходим по всему списку букв
				for(auto & item : letters){
					// Формируем новый список букв
					tmp.emplace(
						alphabet.convert(item.first),
						alphabet.convert(item.second)
					);
				}
				// Выполняем установку букв
				alphabet.setSubstitutes(tmp);
			}
		}
		/**
		 * getTokensUnknown Метод извлечения списка токенов приводимых к <unk>
		 * @return список токенов
		 */
		const set <size_t> getTokensUnknown() noexcept {
			// Результат работы функции
			set <size_t> result;
			// Извлекаем список токенов
			const auto & tokens = alm->getTokensUnknown();
			// Если список токенов получен
			if(!tokens.empty()){
				// Переходим по всему списку токенов
				for(auto & token : tokens) result.emplace(size_t(token));
			}
			// Выводим результат
			return result;
		}
		/**
		 * getSubstitutes Метод извлечения букв для исправления слов из смешанных алфавитов
		 * @param return список букв разных алфавитов соответствующих друг-другу
		 */
		const map <wstring, wstring> getSubstitutes() noexcept {
			// Результат работы функции
			map <wstring, wstring> result;
			// Получаем список букв
			const auto & letters = alphabet.getSubstitutes();
			// Если список букв получен
			if(!letters.empty()){
				// Переходим по всему списку букв
				for(auto & item : letters){
					// Формируем новый список букв
					result.emplace(
						alphabet.convert(item.first),
						alphabet.convert(item.second)
					);
				}
			}
			// Выводим результат
			return result;
		}
		/**
		 * setTokenUnknown Метод установки списка токенов которых нужно идентифицировать как <unk>
		 * @param options список токенов которых нужно идентифицировать как <unk>
		 */
		void setTokenUnknown(const wstring & options) noexcept {
			// Выполняем установку списка токенов которых нужно идентифицировать как <unk>
			alm->setTokenUnknown(alphabet.convert(options));
		}
		/**
		 * switchAllowApostrophe Метод разрешения или запрещения апострофа как части слова
		 */
		void switchAllowApostrophe() noexcept {
			// Выполняем переключение разрешения апострофа
			alphabet.switchAllowApostrophe();
		}
		/**
		 * addBadword Метод добавления идентификатора похого слова в список
		 * @param idw идентификатор слова
		 */
		void addBadword(const size_t idw) noexcept {
			// Выполняем добавление идентификатора похого слова в список
			alm->addBadword(idw);
		}
		/**
		 * addBadword Метод добавления похого слова в список
		 * @param word слово для добавления
		 */
		void addBadword(const wstring & word) noexcept {
			// Выполняем добавление похого слова в список
			alm->addBadword(alphabet.convert(word));
		}
		/**
		 * addGoodword Метод добавления идентификатора хорошего слова в список
		 * @param idw идентификатор слова
		 */
		void addGoodword(const size_t idw) noexcept {
			// Выполняем добавление идентификатора хорошего слова в список
			alm->addGoodword(idw);
		}
		/**
		 * addGoodword Метод добавления хорошего слова в список
		 * @param word слово для добавления
		 */
		void addGoodword(const wstring & word) noexcept {
			// Выполняем добавление хорошего слова в список
			alm->addGoodword(alphabet.convert(word));
		}
		/**
		 * countBigrams Метод проверки количества найденных в тексте биграмм
		 * @param text текст для расчёта
		 * @return     количество найденных биграмм
		 */
		const size_t countBigrams(const wstring & text) noexcept {
			// Выводим результат
			return alm->bigrams(alphabet.convert(text));
		}
		/**
		 * perplexity Метод расчёта перплексии текста
		 * @param  text текст для расчёта
		 * @return      результат расчёта
		 */
		const alm_t::ppl_t perplexity(const wstring & text) noexcept {
			// Выполняем расчёт перплексии
			return alm->perplexity(text);
		}
		/**
		 * countTrigrams Метод проверки количества найденных в тексте триграмм
		 * @param text текст для расчёта
		 * @return     количество найденных триграмм
		 */
		const size_t countTrigrams(const wstring & text) noexcept {
			// Выводим результат
			return alm->trigrams(alphabet.convert(text));
		}
		/**
		 * setBadwords Метод установки списка идентификаторов плохих слов в список
		 * @param idws список идентификаторов плохих слов
		 */
		void setBadwords(const set <size_t> & idws) noexcept {
			// Выполняем установку списка идентификаторов плохих слов в список
			alm->setBadwords(idws);
		}
		/**
		 * setBadwords Метод установки списка плохих слов в список
		 * @param badwords список плохих слов
		 */
		void setBadwords(const vector <wstring> & badwords) noexcept {
			// Список плохих слов
			vector <string> tmp;
			// Формируем новый список
			for(auto & word : badwords) tmp.push_back(alphabet.convert(word));
			// Выполняем установку списка плохих слов в список
			alm->setBadwords(tmp);
		}
		/**
		 * setGoodwords Метод установки списка идентификаторов хороших слов в список
		 * @param idws список идентификаторов хороших слов
		 */
		void setGoodwords(const set <size_t> & idws) noexcept {
			// Выполняем установку списка идентификаторов хороших слов в список
			alm->setGoodwords(idws);
		}
		/**
		 * setGoodwords Метод установки списка хороших слов в список
		 * @param goodwords список хороших слов
		 */
		void setGoodwords(const vector <wstring> & goodwords) noexcept {
			// Список хороших слов
			vector <string> tmp;
			// Формируем новый список
			for(auto & word : goodwords) tmp.push_back(alphabet.convert(word));
			// Выполняем установку списка хороших слов в список
			alm->setGoodwords(tmp);
		}
		/**
		 * countGrams Метод проверки количества найденных в тексте n-грамм
		 * @param text текст для расчёта
		 * @return     количество найденных n-грамм
		 */
		const size_t countGrams(const wstring & text) noexcept {
			// Выводим результат
			return alm->grams(alphabet.convert(text));
		}
		/**
		 * countBigrams Метод проверки количества найденных биграмм
		 * @param seq список последовательностей
		 * @return    количество найденных биграмм
		 */
		const size_t countBigrams(const vector <size_t> & seq) noexcept {
			// Выводим результат
			return alm->bigrams(seq);
		}
		/**
		 * perplexity Метод расчёта перплексии
		 * @param  seq список последовательностей
		 * @return     результат расчёта
		 */
		const alm_t::ppl_t perplexity(const vector <size_t> & seq) noexcept {
			// Выполняем расчёт перплексии
			return alm->perplexity(seq);
		}
		/**
		 * countTrigrams Метод проверки количества найденных триграмм
		 * @param seq список последовательностей
		 * @return    количество найденных триграмм
		 */
		const size_t countTrigrams(const vector <size_t> & seq) noexcept {
			// Выводим результат
			return alm->trigrams(seq);
		}
		/**
		 * countGrams Метод проверки количества найденных n-грамм
		 * @param seq список последовательностей
		 * @return    количество найденных n-грамм
		 */
		const size_t countGrams(const vector <size_t> & seq) noexcept {
			// Выводим результат
			return alm->grams(seq);
		}
		/**
		 * arabic2Roman Метод перевода арабских чисел в римские
		 * @param  number арабское число от 1 до 4999
		 * @return        римское число
		 */
		const wstring arabic2Roman(const size_t number) noexcept {
			// Выполняем конвертацию чисел
			return alphabet.arabic2Roman(number);
		}
		/**
		 * arabic2Roman Метод перевода арабских чисел в римские
		 * @param  word арабское число от 1 до 4999
		 * @return      римское число
		 */
		const wstring arabic2Roman(const wstring & word) noexcept {
			// Выполняем конвертацию чисел
			return alphabet.arabic2Roman(word);
		}
		/**
		 * setLocale Метод установки локали
		 * @param text локализация приложения
		 */
		void setLocale(const wstring & text = L"en_US.UTF-8") noexcept {
			// Устанавливаем локаль
			alphabet.setlocale(alphabet.convert(text));
		}
		/**
		 * ids Метод извлечения идентификатора последовательности
		 * @param  seq последовательность для получения идентификатора
		 * @return     идентификатор последовательности
		 */
		const size_t ids(const vector <size_t> & seq) noexcept {
			// Выводим идентификатор последовательности
			return tokenizer.ids(seq);
		}
		/**
		 * idw Метод извлечения идентификатора слова
		 * @param  word  слово для получения идентификатора
		 * @param  check нужно выполнить дополнительную проверку слова
		 * @return       идентификатор слова
		 */
		const size_t idw(const wstring & word, const bool check = true) noexcept {
			// Выводим идентификатор слова
			return alm->getIdw(word, check);
		}
		/**
		 * setThreads Метод установки количества потоков
		 * @param threads количество потоков для работы
		 */
		void setThreads(const size_t threads = 0) noexcept {
			// Выполняем установку количества потоков
			alm->setThreads(threads);
		}
		/**
		 * clear Метод очистки
		 */
		void clear(clear_t flag = clear_t::all){
			// Выполняем проверку флага
			switch(u_short(flag)){
				// Выполняем полную очистку
				case u_short(clear_t::all): {
					// Выполняем очистику языковой модели
					alm->clear();
					// Выполняем очистику алфавита
					alphabet.clear();
					// Выполняем очистку токенизатора
					tokenizer.clear();
				} break;
				// Выполняем очистку чёрного списка слов
				case u_short(clear_t::badwords): alm->clearBadwords(); break;
				// Выполняем очистку пользовательских токенов
				case u_short(clear_t::utokens): alm->clearUserTokens(); break;
				// Выполняем очистку белого списка слов
				case u_short(clear_t::goodwords): alm->clearGoodwords(); break;
			}
		}
		/**
		 * fti Метод удаления дробной части числа
		 * @param  num   число для обработки
		 * @param  count количество символов после запятой
		 * @return       число без дробной части
		 */
		const size_t fti(const double num, const size_t count = 0) noexcept {
			// Выполняем удаление дробной части
			return tokenizer.fti(num, count);
		}
		/**
		 * context Метод сборки текстового контекста из последовательности
		 * @param seq  последовательность слов для сборки контекста
		 * @param nwrd флаг разрешающий вывод системных токенов
		 * @return     собранный текстовый контекст
		 */
		const wstring context(const vector <size_t> & seq, const bool nwrd = false) noexcept {
			// Выполняем сборку текстового контекста из последовательности
			return alm->context(seq, nwrd);
		}
		/**
		 * readLM Метод чтения данных из файла arpa
		 * @param filename адрес файла для чтения
		 * @param meta     метаданные бинарного контейнера в формате json
		 */
		void readLM(const wstring & filename, const wstring & meta = L"") noexcept {
			// Если адрес файла передан
			if(!filename.empty()){
				// Если это бинарный контейнер
				if(filename.rfind(L".alm") != wstring::npos){
					// Создаём объект бинарного контейнера
					ablm_t ablm(alphabet.convert(filename), alm.get(), &alphabet, &tokenizer, (!logfile.empty() ? logfile.c_str() : nullptr));
					// Если метеданные получены
					if(!meta.empty()){
						// Выполняем конвертацию метаданных
						json data = json::parse(alphabet.convert(meta));
						// Если тип шифрования передан
						if(data.contains("aes") && data.at("aes").is_number()){
							// Тип шифрования
							u_int type = 0;
							// Извлекаем тип шифрования
							data.at("aes").get_to(type);
							// Если размер шифрования получен
							switch(type){
								// Если это 128-и битное шифрование
								case 128: ablm.setAES(aspl_t::types_t::aes128); break;
								// Если это 192-х битное шифрование
								case 192: ablm.setAES(aspl_t::types_t::aes192); break;
								// Если это 256-и битное шифрование
								case 256: ablm.setAES(aspl_t::types_t::aes256); break;
							}
						}
						// Если название словаря передано
						if(data.contains("name") && data.at("name").is_string()){
							// Название словаря
							string name = "";
							// Извлекаем название словаря
							data.at("name").get_to(name);
							// Устанавливаем название словаря
							if(!name.empty()) ablm.setName(name);
						}
						// Если имя автора передано
						if(data.contains("author") && data.at("author").is_string()){
							// Имя автора
							string author = "";
							// Извлекаем имя автора
							data.at("author").get_to(author);
							// Устанавливаем имя автора
							if(!author.empty()) ablm.setAuthor(author);
						}
						// Если тип лицензии передан
						if(data.contains("lictype") && data.at("lictype").is_string()){
							// Тип лицензии
							string lictype = "";
							// Извлекаем тип лицензии
							data.at("lictype").get_to(lictype);
							// Устанавливаем тип лицензии
							if(!lictype.empty()) ablm.setLictype(lictype);
						}
						// Если текст лицензии передан
						if(data.contains("lictext") && data.at("lictext").is_string()){
							// Текст лицензии
							string lictext = "";
							// Извлекаем текст лицензии
							data.at("lictext").get_to(lictext);
							// Устанавливаем текст лицензии
							if(!lictext.empty()) ablm.setLictext(lictext);
						}
						// Если контактные данные переданы
						if(data.contains("contacts") && data.at("contacts").is_string()){
							// Контактные данные
							string contacts = "";
							// Извлекаем контактные данные
							data.at("contacts").get_to(contacts);
							// Устанавливаем контакнтые данные
							if(!contacts.empty()) ablm.setContacts(contacts);
						}
						// Если пароль шифрования контейнера передан
						if(data.contains("password") && data.at("password").is_string()){
							// Пароль контейнера
							string password = "";
							// Извлекаем пароль контейнера
							data.at("password").get_to(password);
							// Устанавливаем пароль контейнера
							if(!password.empty()) ablm.setPassword(password);
						}
						// Если копирайт контейнера передан
						if(data.contains("copyright") && data.at("copyright").is_string()){
							// Копирайт контейнера
							string copyright = "";
							// Извлекаем копирайт контейнера
							data.at("copyright").get_to(copyright);
							// Устанавливаем копирайт контейнера
							if(!copyright.empty()) ablm.setCopyright(copyright);
						}
					}
					// Выполняем инициализацию словаря
					ablm.init();
					// Выполняем чтение бинарных данных
					ablm.readAlm();
				// Иначе если это arpa, загружаем обычным способом
				} else alm->read(alphabet.convert(filename));
			}
		}
		/**
		 * checkSequence Метод проверки существования последовательности
		 * @param text     текст для проверки существования
		 * @param accurate режим точной проверки
		 * @return         результат проверки
		 */
		const pair <bool, size_t> checkSequence(const wstring & text, const bool accurate = false) noexcept {
			// Выполняем проверку существования последовательности
			return alm->check(text, accurate);
		}
		/**
		 * checkSequence Метод проверки существования последовательности, с указанным шагом
		 * @param text текст для проверки существования
		 * @param step размер шага проверки последовательности
		 * @return     результат проверки
		 */
		const bool checkSequence(const wstring & text, const u_short step) noexcept {
			// Выполняем проверку существования последовательности
			return alm->check(text, step);
		}
		/**
		 * checkSequence Метод проверки существования последовательности, с указанным шагом
		 * @param seq  список слов последовательности
		 * @param step размер шага проверки последовательности
		 * @return     результат проверки
		 */
		const bool checkSequence(const vector <wstring> & seq, const u_short step) noexcept {
			// Выполняем проверку существования последовательности
			return alm->check(seq, step);
		}
		/**
		 * checkSequence Метод проверки существования последовательности, с указанным шагом
		 * @param seq  список слов последовательности
		 * @param step размер шага проверки последовательности
		 * @return     результат проверки
		 */
		const bool checkSequence(const vector <size_t> & seq, const u_short step) noexcept {
			// Выполняем проверку существования последовательности
			return alm->check(seq, step);
		}
		/**
		 * existSequence Метод проверки существования последовательности, с указанным шагом
		 * @param text текст для проверки существования
		 * @param step размер шага проверки последовательности
		 * @return     результат проверки
		 */
		const pair <bool, size_t> existSequence(const wstring & text, const u_short step) noexcept {
			// Выполняем проверку существования последовательности
			return alm->exist(text, step);
		}
		/**
		 * existSequence Метод проверки существования последовательности, с указанным шагом
		 * @param seq  список слов последовательности
		 * @param step размер шага проверки последовательности
		 * @return     результат проверки
		 */
		const pair <bool, size_t> existSequence(const vector <wstring> & seq, const u_short step) noexcept {
			// Выполняем проверку существования последовательности
			return alm->exist(seq, step);
		}
		/**
		 * existSequence Метод проверки существования последовательности, с указанным шагом
		 * @param seq  список слов последовательности
		 * @param step размер шага проверки последовательности
		 * @return     результат проверки
		 */
		const pair <bool, size_t> existSequence(const vector <size_t> & seq, const u_short step) noexcept {
			// Выполняем проверку существования последовательности
			return alm->exist(seq, step);
		}
		/**
		 * check Метод проверки строки
		 * @param str  строка для проверки
		 * @param flag флаг выполняемой проверки
		 * @return     результат проверки
		 */
		const bool check(const wstring & str, const check_t flag = check_t::letter) noexcept {
			// Переводим слово в нижний регистр
			const wstring & tmp = alphabet.toLower(str);
			// Выполняем проверку флага
			switch(u_short(flag)){
				// Выполняем проверку на Дом-2
				case u_short(check_t::home2): return alphabet.checkHome2(tmp);
				// Выполняем проверку на наличии латинского символа
				case u_short(check_t::latian): return alphabet.checkLatian(tmp);
				// Выполняем проверку на наличии дефиса
				case u_short(check_t::hyphen): return alphabet.checkHyphen(tmp);
				// Выполняем проверку легальности буквы
				case u_short(check_t::letter): return alphabet.check(tmp.front());
				// Выполняем проверку на симиляции букв с другими языками
				case u_short(check_t::similars): return alphabet.checkSimilars(tmp);
			}
			// Выводим результат по умолчанию
			return false;
		}
		/**
		 * match Метод проверки соответствия строки
		 * @param str  строка для проверки
		 * @param flag флаг типа проверки
		 * @return     результат проверки
		 */
		const bool match(const wstring & str, const match_t flag = match_t::allowed) noexcept {
			// Переводим слово в нижний регистр
			const wstring & tmp = alphabet.toLower(str);
			// Выполняем проверку флага
			switch(u_short(flag)){
				// Выполняем проверку на соответствие слова url адресу
				case u_short(match_t::url): return alphabet.isUrl(tmp);
				// Выполняем проверку на соответствие слова аббревиатуре
				case u_short(match_t::abbr): return tokenizer.isAbbr(tmp);
				// Выполняем проверку является ли строка латиницей
				case u_short(match_t::latian): return alphabet.isLatian(tmp);
				// Выполняем проверку на соответствие слова числу
				case u_short(match_t::number): return alphabet.isNumber(tmp);
				// Выполняем проверку на соответствие слова псевдо-числу
				case u_short(match_t::anumber): return alphabet.isANumber(tmp);
				// Выполняем проверку на соответствие слова словарю
				case u_short(match_t::allowed): return alphabet.isAllowed(tmp);
				// Выполняем проверку на соответствие слова дробному числу
				case u_short(match_t::decimal): return alphabet.isDecimal(tmp);
				// Выполняем проверку на определение математических операий
				case u_short(match_t::math): return alphabet.isMath(tmp.front());
				// Выполняем проверку на символ верхнего регистра
				case u_short(match_t::upper): return alphabet.isUpper(str.front());
				// Выполняем проверку является ли буква, знаком препинания
				case u_short(match_t::punct): return alphabet.isPunct(tmp.front());
				// Выполняем проверку является ли буква пробелом
				case u_short(match_t::space): return alphabet.isSpace(tmp.front());
				// Выполняем проверку является ли буква спец-символом
				case u_short(match_t::special): return alphabet.isSpecial(tmp.front());
				// Выполняем проверку является ли буква символом изоляции
				case u_short(match_t::isolation): return alphabet.isIsolation(tmp.front());
			}
			// Выводим результат по умолчанию
			return false;
		}
		/**
		 * findByFiles Метод поиска n-грамм в текстовом файле
		 * @param path     адрес каталога или файла для обработки
		 * @param filename адрес файла для записи результата
		 * @param ext      расширение файлов в каталоге (если адрес передан каталога)
		 */
		void findByFiles(const wstring & path, const wstring & filename, const wstring & ext = L"txt") noexcept {
			// Выполняем поиск n-грамм в текстовом файле
			alm->findByFiles(alphabet.convert(path), alphabet.convert(filename), nullptr, alphabet.convert(ext));
		}
		/**
		 * pplByFiles Метод чтения расчёта перплексии по файлу или группе файлов
		 * @param path адрес каталога или файла для расчёта перплексии
		 * @param ext  расширение файлов в каталоге (если адрес передан каталога)
		 * @return     результат расчёта
		 */
		const alm_t::ppl_t pplByFiles(const wstring & path, const wstring & ext = L"txt") noexcept {
			// Выполняем расчёт перплексии
			return alm->pplByFiles(alphabet.convert(path), nullptr, alphabet.convert(ext));
		}
		/**
		 * delInText Метод очистки текста
		 * @param text текст для очистки
		 * @param flag флаг критерия очистки
		 * @return     текст без запрещенных символов
		 */
		const wstring delInText(const wstring & text, const wdel_t flag = wdel_t::broken) noexcept {
			// Выполняем проверку флага
			switch(u_short(flag)){
				// Выполняем удаление знаков пунктуации в тексте
				case u_short(wdel_t::punct): return alphabet.delPunctInWord(text);
				// Выполняем удаление всех символов кроме разрешенных
				case u_short(wdel_t::broken): return alphabet.delBrokenInWord(text);
				// Выполняем удаление весх дефисов в тексте
				case u_short(wdel_t::hyphen): return alphabet.delHyphenInWord(text);
			}
			// Выводим результат по умолчанию
			return text;
		}
		/**
		 * checkSequence Метод проверки существования последовательности
		 * @param seq      список слов последовательности
		 * @param accurate режим точной проверки
		 * @return         результат проверки
		 */
		const pair <bool, size_t> checkSequence(const vector <size_t> & seq, const bool accurate = false) noexcept {
			// Выполняем проверку существования последовательности
			return alm->check(seq, accurate);
		}
		/**
		 * checkSequence Метод проверки существования последовательности
		 * @param seq      список слов последовательности
		 * @param accurate режим точной проверки
		 * @return         результат проверки
		 */
		const pair <bool, size_t> checkSequence(const vector <wstring> & seq, const bool accurate = false) noexcept {
			// Выполняем проверку существования последовательности
			return alm->check(seq, accurate);
		}
		/**
		 * sentencesToFile Метод сборки указанного количества предложений и записи в файл
		 * @param counts   количество предложений для сборки
		 * @param filename адрес файла для записи результата
		 */
		void sentencesToFile(const size_t counts, const wstring & filename) noexcept {
			// Выполняем сборку указанного количества предложений
			alm->sentencesToFile(counts, alphabet.convert(filename));
		}
		/**
		 * fixUppersByFiles Метод исправления регистров текста в текстовом файле
		 * @param path     адрес каталога или файла для обработки
		 * @param filename адрес файла для записи результата
		 * @param ext      расширение файлов в каталоге (если адрес передан каталога)
		 */
		void fixUppersByFiles(const wstring & path, const wstring & filename, const wstring & ext = L"txt") noexcept {
			// Выполняем исправление регистров текста
			alm->fixUppersByFiles(alphabet.convert(path), alphabet.convert(filename), nullptr, alphabet.convert(ext));
		}
		/**
		 * countsByFiles Метод подсчёта количества n-грамм в текстовом файле
		 * @param path     адрес каталога или файла для обработки
		 * @param filename адрес файла для записи результата
		 * @param ngrams   размер n-граммы для подсчёта
		 * @param ext      расширение файлов в каталоге (если адрес передан каталога)
		 */
		void countsByFiles(const wstring & path, const wstring & filename, const u_short ngrams = 0, const wstring & ext = L"txt") noexcept {
			// Выполняем подсчёт количества n-грамм
			alm->countsByFiles(alphabet.convert(path), alphabet.convert(filename), ngrams, nullptr, alphabet.convert(ext));
		}
		/**
		 * checkByFiles Метод проверки существования последовательности в текстовом файле
		 * @param path     адрес каталога или файла для обработки
		 * @param filename адрес файла для записи результата
		 * @param accurate режим точной проверки
		 * @param ext      расширение файлов в каталоге (если адрес передан каталога)
		 */
		void checkByFiles(const wstring & path, const wstring & filename, const bool accurate = false, const wstring & ext = L"txt") noexcept {
			// Выполняем проверку существования последовательности
			alm->checkByFiles(alphabet.convert(path), alphabet.convert(filename), accurate, nullptr, alphabet.convert(ext));
		}
		/**
		 * setTokenizerFn Метод установки функции внешнего токенизатора
		 * @param fn функция внешнего токенизатора
		 */
		void setTokenizerFn(function <void (const wstring &, function <const bool (const wstring &, const vector <string> &, const bool, const bool)>)> fn) noexcept {
			// Устанавливаем функцию внешнего токенизатора
			tokenizer.setExternal(fn);
		}
	};
};
// alm Регистрируем имя модуля языковой модели
PYBIND11_MODULE(alm, m) {
	/**
	 * Устанавливаем флаги библиотеки
	 */
	// Список флагов для удаления в тексе символов
	py::enum_ <anyks::wdel_t> (m, "wdel_t")
	.value("punct", anyks::wdel_t::punct)
	.value("broken", anyks::wdel_t::broken)
	.value("hyphen", anyks::wdel_t::hyphen)
	.export_values();
	// Список флагов для проверки текста
	py::enum_ <anyks::check_t> (m, "check_t")
	.value("home2", anyks::check_t::home2)
	.value("latian", anyks::check_t::latian)
	.value("hyphen", anyks::check_t::hyphen)
	.value("letter", anyks::check_t::letter)
	.value("similars", anyks::check_t::similars)
	.export_values();
	// Список флагов для очистки текста
	py::enum_ <anyks::clear_t> (m, "clear_t")
	.value("all", anyks::clear_t::all)
	.value("utokens", anyks::clear_t::utokens)
	.value("badwords", anyks::clear_t::badwords)
	.value("goodwords", anyks::clear_t::goodwords)
	.export_values();
	// Список флагов для матчинга текста
	py::enum_ <anyks::match_t> (m, "match_t")
	.value("url", anyks::match_t::url)
	.value("abbr", anyks::match_t::abbr)
	.value("math", anyks::match_t::math)
	.value("upper", anyks::match_t::upper)
	.value("punct", anyks::match_t::punct)
	.value("space", anyks::match_t::space)
	.value("latian", anyks::match_t::latian)
	.value("number", anyks::match_t::number)
	.value("anumber", anyks::match_t::anumber)
	.value("allowed", anyks::match_t::allowed)
	.value("decimal", anyks::match_t::decimal)
	.value("special", anyks::match_t::special)
	.value("isolation", anyks::match_t::isolation)
	.export_values();
	// Список флагов основных опций библиотеки
	py::enum_ <anyks::options_t> (m, "options_t")
	.value("debug", anyks::options_t::debug)
	.value("stress", anyks::options_t::stress)
	.value("uppers", anyks::options_t::uppers)
	.value("collect", anyks::options_t::collect)
	.value("onlyGood", anyks::options_t::onlyGood)
	.value("mixdicts", anyks::options_t::mixdicts)
	.value("confidence", anyks::options_t::confidence)
	.export_values();
	// Структура параметров расчёта перплексии
	py::class_ <anyks::alm_t::ppl_t> (m, "ppl_t")
	.def(py::init())
	.def_readwrite("oovs", &anyks::alm_t::ppl_t::oovs)
	.def_readwrite("words", &anyks::alm_t::ppl_t::words)
	.def_readwrite("sentences", &anyks::alm_t::ppl_t::sentences)
	.def_readwrite("zeroprobs", &anyks::alm_t::ppl_t::zeroprobs)
	.def_readwrite("logprob", &anyks::alm_t::ppl_t::logprob)
	.def_readwrite("ppl", &anyks::alm_t::ppl_t::ppl)
	.def_readwrite("ppl1", &anyks::alm_t::ppl_t::ppl1);
	/**
	 * Устанавливаем методы объекта
	 */
	{
		// idt Метод извлечения идентификатора токена
		m.def("idt", &anyks::Methods::idt, "Token ID retrieval method")
		// ids Метод извлечения идентификатора последовательности
		.def("ids", &anyks::Methods::ids, "Sequence ID retrieval method")
		// setZone Метод установки пользовательской зоны
		.def("setZone", &anyks::Methods::setZone, "User zone set method")
		// setAlphabet Метод установки алфавита
		.def("setAlphabet", &anyks::Methods::setAlphabet, "Method set Alphabet")
		// setUnknown Метод установки неизвестного слова
		.def("setUnknown", &anyks::Methods::setUnknown, "Method set unknown word")
		// getName Метод извлечения названия библиотеки
		.def("getName", &anyks::Methods::getName, "Library name retrieval method")
		// isToken Метод проверки идентификатора на токен
		.def("isToken", &anyks::Methods::isToken, "Checking a word against a token")
		// sentences Метод генерации предложений
		.def("sentences", &anyks::Methods::sentences, "Sentences generation method")
		// getEmail Метод извлечения электронной почты автора
		.def("getEmail", &anyks::Methods::getEmail, "Author email retrieval method")
		// getPhone Метод извлечения телефона автора
		.def("getPhone", &anyks::Methods::getPhone, "Author phone retrieval method")
		// getAuthor Метод извлечения имени автора
		.def("getAuthor", &anyks::Methods::getAuthor, "Author name retrieval method")
		// find Метод поиска n-грамм в тексте
		.def("findNgram", &anyks::Methods::findNgram, "N-gram search method in text")
		// isIdWord Метод проверки на соответствие идентификатора слову
		.def("isIdWord", &anyks::Methods::isIdWord, "Checking a token against a word")
		// setOption Метод установки опций модуля языковой модели
		.def("setOption", &anyks::Methods::setOption, "Method for set module options")
		// getUnknown Метод извлечения неизвестного слова
		.def("getUnknown", &anyks::Methods::getUnknown, "Method extraction unknown word")
		// size Метод получения размера n-грамы
		.def("size", &anyks::Methods::size, "Method of obtaining the size of the N-gram")
		// jsonToText Метод преобразования текста в формате json в текст
		.def("jsonToText", &anyks::Methods::jsonToText, "Method to convert JSON to text")
		// textToJson Метод преобразования текста в json
		.def("textToJson", &anyks::Methods::textToJson, "Method to convert text to JSON")
		// restore Метод восстановления текста из контекста
		.def("restore", &anyks::Methods::restore, "Method for restore text from context")
		// unsetOption Метод отключения опции модуля
		.def("unsetOption", &anyks::Methods::unsetOption, "Disable module option method")
		// getBadwords Метод извлечения чёрного списка
		.def("getBadwords", &anyks::Methods::getBadwords, "Method get words in blacklist")
		// setUserToken Метод добавления токена пользователя
		.def("setUserToken", &anyks::Methods::setUserToken, "Method for adding user token")
		// getGoodwords Метод извлечения белого списка
		.def("getGoodwords", &anyks::Methods::getGoodwords, "Method get words in whitelist")
		// setLogfile Метод установки файла для вывода логов
		.def("setLogfile", &anyks::Methods::setLogfile, "Method of set the file for log output")
		// setOOvFile Метод установки файла для сохранения OOV слов
		.def("setOOvFile", &anyks::Methods::setOOvFile, "Method set file for saving OOVs words")
		// pplConcatenate Метод объединения перплексий
		.def("pplConcatenate", &anyks::Methods::pplConcatenate, "Method of combining perplexia")
		// getUserTokens Метод извлечения списка пользовательских токенов
		.def("getUserTokens", &anyks::Methods::getUserTokens, "User token list retrieval method")
		// allowStress Метод разрешения, использовать ударение в словах
		.def("allowStress", &anyks::Methods::allowStress, "Method for allow using stress in words")
		// tokenization Метод разбивки текста на токены
		.def("tokenization", &anyks::Methods::tokenization, "Method for breaking text into tokens")
		// fixUppers Метод исправления регистров в тексте
		.def("fixUppers", &anyks::Methods::fixUppers, "Method for correcting registers in the text")
		// checkHypLat Метод поиска дефиса и латинского символа
		.def("checkHypLat", &anyks::Methods::checkHypLat, "Hyphen and latin character search method")
		// getContact Метод извлечения контактных данных автора
		.def("getContact", &anyks::Methods::getContact, "Author contact information retrieval method")
		// getSite Метод извлечения адреса сайта автора
		.def("getSite", &anyks::Methods::getSite, "Method for extracting the author’s website address")
		// getAlphabet Метод получения алфавита языка
		.def("getAlphabet", &anyks::Methods::getAlphabet, "Method for obtaining the language alphabet")
		// urls Метод извлечения координат url адресов в строке
		.def("urls", &anyks::Methods::urls, "Method for extracting URL address coordinates in a string")
		// getVersion Метод получения версии языковой модели
		.def("getVersion", &anyks::Methods::getVersion, "Method for obtaining the language model version")
		// isAllowApostrophe Метод проверки разрешения апострофа
		.def("isAllowApostrophe", &anyks::Methods::isAllowApostrophe, "Apostrophe permission check method")
		// disallowStress Метод запрещения использовать ударение в словах
		.def("disallowStress", &anyks::Methods::disallowStress, "Method for disallow using stress in words")
		// getUserTokenId Метод получения идентификатора пользовательского токена
		.def("getUserTokenId", &anyks::Methods::getUserTokenId, "Method for obtaining user token identifier")
		// roman2Arabic Метод перевода римских цифр в арабские
		.def("roman2Arabic", &anyks::Methods::roman2Arabic, "Method for translating Roman numerals to Arabic")
		// rest Метод исправления и детектирования слов со смешанными алфавитами
		.def("rest", &anyks::Methods::rest, "Method for correction and detection of words with mixed alphabets")
		// setTokensDisable Метод установки списка запрещённых токенов
		.def("setTokensDisable", &anyks::Methods::setTokensDisable, "Method for set the list of forbidden tokens")
		// setTokenDisable Метод установки списка не идентифицируемых токенов
		.def("setTokenDisable", &anyks::Methods::setTokenDisable, "Method for set the list of unidentifiable tokens")
		// setAllTokenDisable Метод установки всех токенов как не идентифицируемых
		.def("setAllTokenDisable", &anyks::Methods::setAllTokenDisable, "Method for set all tokens as unidentifiable")
		// setTokensUnknown Метод установки списка токенов приводимых к <unk>
		.def("setTokensUnknown", &anyks::Methods::setTokensUnknown, "Method for set the list of tokens cast to <unk>")
		// setTokenizerFn Метод установки функции внешнего токенизатора
		.def("setTokenizerFn", &anyks::Methods::setTokenizerFn, "Method for set the function of an external tokenizer")
		// getTokensDisable Метод извлечения списка запрещённых токенов
		.def("getTokensDisable", &anyks::Methods::getTokensDisable, "Method for retrieving the list of forbidden tokens")
		// countLetter Метод подсчета количества указанной буквы в слове
		.def("countLetter", &anyks::Methods::countLetter, "Method for counting the amount of a specific letter in a word")
		// setAllTokenUnknown Метод установки всех токенов идентифицируемых как <unk>
		.def("setAllTokenUnknown", &anyks::Methods::setAllTokenUnknown, "The method of set all tokens identified as <unk>")
		// countAlphabet Метод получения количества букв в словаре
		.def("countAlphabet", &anyks::Methods::countAlphabet, "Method of obtaining the number of letters in the dictionary")
		// getUserTokenWord Метод получения пользовательского токена по его идентификатору
		.def("getUserTokenWord", &anyks::Methods::getUserTokenWord, "Method for obtaining a custom token by its identifier")
		// setUserTokenMethod Метод добавления функции обработки пользовательского токена
		.def("setUserTokenMethod", &anyks::Methods::setUserTokenMethod, "Method for set a custom token processing function")
		// setSubstitutes Метод установки букв для исправления слов из смешанных алфавитов
		.def("setSubstitutes", &anyks::Methods::setSubstitutes, "Method for set letters to correct words from mixed alphabets")
		// getTokensUnknown Метод извлечения списка токенов приводимых к <unk>
		.def("getTokensUnknown", &anyks::Methods::getTokensUnknown, "Method for extracting a list of tokens reducible to <unk>")
		// getSubstitutes Метод извлечения букв для исправления слов из смешанных алфавитов
		.def("getSubstitutes", &anyks::Methods::getSubstitutes, "Method of extracting letters to correct words from mixed alphabets")
		// setTokenUnknown Метод установки списка токенов которых нужно идентифицировать как <unk>
		.def("setTokenUnknown", &anyks::Methods::setTokenUnknown, "Method of set the list of tokens that need to be identified as <unk>")
		// setWordPreprocessingMethod Метод установки функции препроцессинга слова
		.def("setWordPreprocessingMethod", &anyks::Methods::setWordPreprocessingMethod, "Method for set the word preprocessing function")
		// switchAllowApostrophe Метод разрешения или запрещения апострофа как части слова
		.def("switchAllowApostrophe", &anyks::Methods::switchAllowApostrophe, "Method for permitting or denying an apostrophe as part of a word");
	} {
		// addAbbr Метод добавления аббревиатуры в виде идентификатора
		m.def("addAbbr", overload_cast_ <const size_t> ()(&anyks::Methods::addAbbr), "Method add abbreviation")
		// addAbbr Метод добавления аббревиатуры в виде слова
		.def("addAbbr", overload_cast_ <const wstring &> ()(&anyks::Methods::addAbbr), "Method add abbreviation")
		// addBadword Метод добавления похого слова в список
		.def("addBadword", overload_cast_ <const wstring &> ()(&anyks::Methods::addBadword), "Method add bad word")
		// addGoodIdw Метод добавления идентификатора похого слова в список
		.def("addBadword", overload_cast_ <const size_t> ()(&anyks::Methods::addBadword), "Method add bad idw word")
		// perplexity Метод расчёта перплексии текста
		.def("perplexity", overload_cast_ <const wstring &> ()(&anyks::Methods::perplexity), "Perplexity calculation")
		// addGoodword Метод добавления идентификатора хорошего слова в список
		.def("addGoodword", overload_cast_ <const wstring &> ()(&anyks::Methods::addGoodword), "Method add good word")
		// addGoodword Метод добавления хорошего слова в список
		.def("addGoodword", overload_cast_ <const size_t> ()(&anyks::Methods::addGoodword), "Method add good idw word")
		// setAbbrs Метод установки списка идентификаторов аббревиатур
		.def("setAbbrs", overload_cast_ <const set <size_t> &> ()(&anyks::Methods::setAbbrs), "Method set abbreviations")
		// isAbbr Метод проверки слова на соответствие аббревиатуры
		.def("isAbbr", overload_cast_ <const size_t> ()(&anyks::Methods::isAbbr), "Checking a word against a abbreviation")
		// countBigrams Метод проверки количества найденных биграмм
		.def("countBigrams", overload_cast_ <const wstring &> ()(&anyks::Methods::countBigrams), "Method get count bigrams")
		// perplexity Метод расчёта перплексии текста
		.def("perplexity", overload_cast_ <const vector <size_t> &> ()(&anyks::Methods::perplexity), "Perplexity calculation")
		// isAbbr Метод проверки слова на соответствие аббревиатуры
		.def("isAbbr", overload_cast_ <const wstring &> ()(&anyks::Methods::isAbbr), "Checking a word against a abbreviation")
		// countTrigrams Метод проверки количества найденных триграмм
		.def("countTrigrams", overload_cast_ <const wstring &> ()(&anyks::Methods::countTrigrams), "Method get count trigrams")
		// Метод добавления идентификатора суффикса цифровой аббреувиатуры
		.def("addSuffix", overload_cast_ <const size_t> ()(&anyks::Methods::addSuffix), "Method add number suffix abbreviation")
		// countGrams Метод проверки количества найденных n-грамм
		.def("countGrams", overload_cast_ <const wstring &> ()(&anyks::Methods::countGrams), "Method get count N-gram by lm size")
		// countBigrams Метод проверки количества найденных биграмм
		.def("countBigrams", overload_cast_ <const vector <size_t> &> ()(&anyks::Methods::countBigrams), "Method get count bigrams")
		// arabic2Roman Метод перевода арабских чисел в римские
		.def("arabic2Roman", overload_cast_ <const size_t> ()(&anyks::Methods::arabic2Roman), "Convert arabic number to roman number")
		// countTrigrams Метод проверки количества найденных триграмм
		.def("countTrigrams", overload_cast_ <const vector <size_t> &> ()(&anyks::Methods::countTrigrams), "Method get count trigrams")
		// setBadwords Метод установки списка идентификаторов плохих слов в список
		.def("setBadwords", overload_cast_ <const set <size_t> &> ()(&anyks::Methods::setBadwords), "Method set idw words to blacklist")
		// setBadwords Метод установки списка плохих слов в список
		.def("setBadwords", overload_cast_ <const vector <wstring> &> ()(&anyks::Methods::setBadwords), "Method set words to blacklist")
		// arabic2Roman Метод перевода арабских чисел в римские
		.def("arabic2Roman", overload_cast_ <const wstring &> ()(&anyks::Methods::arabic2Roman), "Convert arabic number to roman number")
		// setGoodwords Метод установки списка идентификаторов хороших слов в список
		.def("setGoodwords", overload_cast_ <const set <size_t> &> ()(&anyks::Methods::setGoodwords), "Method set idw words to whitelist")
		// setGoodwords Метод установки списка хороших слов в список
		.def("setGoodwords", overload_cast_ <const vector <wstring> &> ()(&anyks::Methods::setGoodwords), "Method set words to whitelist")
		// countGrams Метод проверки количества найденных n-грамм
		.def("countGrams", overload_cast_ <const vector <size_t> &> ()(&anyks::Methods::countGrams), "Method get count N-gram by lm size")
		// setSuffixes Метод установки списка идентификаторов аббревиатур
		.def("setSuffixes", overload_cast_ <const set <size_t> &> ()(&anyks::Methods::setSuffixes), "Method set number suffix abbreviations")
		// isSuffix Метод проверки слова на суффикс цифровой аббревиатуры
		.def("isSuffix", overload_cast_ <const wstring &> ()(&anyks::Methods::isSuffix), "Checking a word against a number suffix abbreviation")
		// getUppers Метод извлечения регистров для каждого слова
		.def("getUppers", overload_cast_ <const vector <size_t> &> ()(&anyks::Methods::getUppers), "Method for extracting registers for each word");
	} {
		// setLocale Метод установки локали
		m.def("setLocale", &anyks::Methods::setLocale, "Method set locale", py::arg("text") = L"en_US.UTF-8")
		// idw Метод извлечения идентификатора слова
		.def("idw", &anyks::Methods::idw, "Word ID retrieval method", py::arg("word") = L"", py::arg("check") = true)
		// setThreads Метод установки количества потоков
		.def("setThreads", &anyks::Methods::setThreads, "Method for set the number of threads", py::arg("threads") = 0)
		// read Метод чтения данных из файла arpa
		.def("readLM", &anyks::Methods::readLM, "Method for reading data from arpa file", py::arg("filename") = L"", py::arg("meta") = L"")
		// fti Метод удаления дробной части числа
		.def("fti", &anyks::Methods::fti, "Method for removing the fractional part of a number", py::arg("num") = 0.0, py::arg("count") = 0)
		// clear Метод очистки
		.def("clear", overload_cast_ <const anyks::clear_t> ()(&anyks::Methods::clear), "Method clear all data", py::arg("flag") = anyks::clear_t::all)
		// context Метод сборки текстового контекста из последовательности
		.def("context", &anyks::Methods::context, "Method for assembling text context from a sequence", py::arg("seq") = vector <size_t> (), py::arg("nwrd") = false)
		// findByFiles Метод поиска n-грамм в текстовом файле
		.def("findByFiles", &anyks::Methods::findByFiles, "Method search N-grams in a text file", py::arg("path") = L"", py::arg("filename") = L"", py::arg("ext") = L"txt")
		// pplByFiles Метод чтения расчёта перплексии по файлу или группе файлов
		.def("pplByFiles", &anyks::Methods::pplByFiles, "Method for reading perplexity calculation by file or group of files", py::arg("path") = L"", py::arg("ext") = L"txt")
		// checkSequence Метод проверки существования последовательности
		.def("checkSequence", overload_cast_ <const wstring &, const u_short> ()(&anyks::Methods::checkSequence), "Sequence Existence Method", py::arg("text") = L"", py::arg("step") = 2)
		// existSequence Метод проверки существования последовательности, без учёта токенов не являющимися словами
		.def("existSequence", overload_cast_ <const wstring &, const u_short> ()(&anyks::Methods::existSequence), "Sequence Existence Method", py::arg("text") = L"", py::arg("step") = 2)
		// checkSequence Метод проверки существования последовательности
		.def("checkSequence", overload_cast_ <const wstring &, const bool> ()(&anyks::Methods::checkSequence), "Sequence Existence Method", py::arg("text") = L"", py::arg("accurate") = false)
		// check Метод проверки строки
		.def("check", overload_cast_ <const wstring &, const anyks::check_t> ()(&anyks::Methods::check), "String Check Method", py::arg("str") = L"", py::arg("flag") = anyks::check_t::letter)
		// match Метод проверки соответствия строки
		.def("match", overload_cast_ <const wstring &, const anyks::match_t> ()(&anyks::Methods::match), "String Matching Method", py::arg("str") = L"", py::arg("flag") = anyks::match_t::allowed)
		// sentencesToFile Метод сборки указанного количества предложений и записи в файл
		.def("sentencesToFile", &anyks::Methods::sentencesToFile, "Method for assembling a specified number of sentences and writing to a file", py::arg("counts") = 0, py::arg("filename") = L"")
		// fixUppersByFiles Метод исправления регистров текста в текстовом файле
		.def("fixUppersByFiles", &anyks::Methods::fixUppersByFiles, "Method for correcting text registers in a text file", py::arg("path") = L"", py::arg("filename") = L"", py::arg("ext") = L"txt")
		// Метод добавления идентификатора суффикса цифровой аббреувиатуры
		.def("addSuffix", overload_cast_ <const wstring &, const size_t> ()(&anyks::Methods::addSuffix), "Method add number suffix abbreviation", py::arg("word") = L"", py::arg("idw") = anyks::idw_t::NIDW)
		// checkSequence Метод проверки существования последовательности
		.def("checkSequence", overload_cast_ <const vector <size_t> &, const u_short> ()(&anyks::Methods::checkSequence), "Sequence Existence Method", py::arg("seq") = vector <size_t> (), py::arg("step") = 2)
		// checkSequence Метод проверки существования последовательности, без учёта токенов не являющимися словами
		.def("existSequence", overload_cast_ <const vector <size_t> &, const u_short> ()(&anyks::Methods::existSequence), "Sequence Existence Method", py::arg("seq") = vector <size_t> (), py::arg("step") = 2)
		// checkSequence Метод проверки существования последовательности
		.def("checkSequence", overload_cast_ <const vector <wstring> &, const u_short> ()(&anyks::Methods::checkSequence), "Sequence Existence Method", py::arg("seq") = vector <wstring> (), py::arg("step") = 2)
		// checkSequence Метод проверки существования последовательности, без учёта токенов не являющимися словами
		.def("existSequence", overload_cast_ <const vector <wstring> &, const u_short> ()(&anyks::Methods::existSequence), "Sequence Existence Method", py::arg("seq") = vector <wstring> (), py::arg("step") = 2)
		// delInText Метод очистки текста
		.def("delInText", overload_cast_ <const wstring &, const anyks::wdel_t> ()(&anyks::Methods::delInText), "Method for delete letter in text", py::arg("text") = L"", py::arg("flag") = anyks::wdel_t::broken)
		// checkSequence Метод проверки существования последовательности
		.def("checkSequence", overload_cast_ <const vector <size_t> &, const bool> ()(&anyks::Methods::checkSequence), "Sequence Existence Method", py::arg("seq") = vector <size_t> (), py::arg("accurate") = false)
		// checkSequence Метод проверки существования последовательности
		.def("checkSequence", overload_cast_ <const vector <size_t> &, const bool> ()(&anyks::Methods::checkSequence), "Sequence Existence Method", py::arg("seq") = vector <wstring> (), py::arg("accurate") = false)
		// countsByFiles Метод подсчёта количества n-грамм в текстовом файле
		.def("countsByFiles", &anyks::Methods::countsByFiles, "Method for counting the number of n-grams in a text file", py::arg("path") = L"", py::arg("filename") = L"", py::arg("ngrams") = 0, py::arg("ext") = L"txt")
		// checkByFiles Метод проверки существования последовательности в текстовом файле
		.def("checkByFiles", &anyks::Methods::checkByFiles, "Method for checking if a sequence exists in a text file", py::arg("path") = L"", py::arg("filename") = L"", py::arg("accurate") = false, py::arg("ext") = L"txt");
	}
};

#endif // _ANYKS_LM_
