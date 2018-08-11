//
//  Config.swift
//  Client
//
//  Created by Dmitriy Kudrin on 22.06.15.
//  Copyright © 2015 Gootax. All rights reserved.
//

import Foundation


/** COMMON SETTINGS **/
// Это демо-версия, будут включены все настройки, если true
public let isDemo = false
// сервер utap или prod
public let prodServer = true
// ID Арендатора
public let gxDefTenantID = "964"
// Версия Client API
public let versionClient = "1.19.4"
// секретный ключ
public let gxSecretKey = "45678223698741maxs24" // 13131313 | 45678223698741maxs24
// Id приложения
public let appId = ""
// Разрешить выбор страны при авторизации
public let withCountry = true
// Url для запросов к килентскому API
//"https://ca.uatgootax.ru:8089/"//"http://ca1.artem.taxi.lcl/" //https://ca2.gootax.pro:8089 //ca.uat.taxi.ru
public let baseUrl = "https://ca2.gootax.pro:8089/"


/** METRICS SETTINGS **/
// Yandex Metrica API key
public let yandexMetricaAPIkey = "dbf8f983-2a03-49f3-8890-55b685de6e2b"


/** LANGUAGE SETTINGS **/
// стандартный язык
public let defaultLanguage = "ru"
// стандартная страна
func defaultCountry() -> Dictionary<String, AnyObject> {
    return ["mask" : "+7({ddd}){ddd}-{dd}-{dd}","placeholder" : "+7(___)___-__-__","minLength" : 11,"shortMask" : "+7","label" : getStringByKey("country.ru"),"code" : "RU"]
}

let languages = ["en", "ru", "me", "it", "de"]
let supportedLang = [
    ["code" : "ru",
        "title" : lanRu()],
    ["code" : "en",
        "title" : lanEnglish()],
    ["code" : "de",
        "title" : lanDe()],
    ["code" : "it",
        "title" : lanIt()],
    ["code" : "fa",
        "title" : lanFa()],
    ["code" : "sr",
        "title" : lanRu()],
    ["code" : "sr-ME",
        "title" : lanRu()],
    ["code" : "tk",
        "title" : lanTk()],
    ["code" : "uz",
        "title" : lanUz()],
    ["code" : "ka",
        "title" : lanKa()],
    ["code" : "fa",
        "title" : lanFa()],
    ["code" : "az",
        "title" : lanAz()]
];

/** THEME SETTINGS **/


/** CALENDAR SETTINGS **/
// 0 - Gregorian | 1 - Persian
public let useCalendarExtensions = false
public let defaultCalendar = 0
public let calendars = [strCalndarGregorian(), strCalndarPersian()]


/** MAPS SETTINGS **/
// стандартная карта
/* 0 - OSM | 1 - Google */
public let defaultMap = 1
/* true - Normal | false - Hybrid */
public let defaultGoogleType = true
// Наличее карт
public let needOSMMap = true
public let needGoogleMapNormal = true
public let needGoogleMapHybrid = true


/** SEARCH SETTINGS **/
// использовать search или autocomplete
public let useSearch = false
public let mapRadius = "0.1" // Радиус поиска по карте
public let listRadius = "1" // Радиус для ближайших адресов
public let searchRadius = "40" // Радиус для автокомплита
public let getCarsRadius = "3000" // Радиус поиска машин в метрах
// Зона приема заказов (в метрах) работает только когда нет полигона, иначе приоритетней полигон
public let ordersZone = 40000


/** PHOTO SETTINGS **/
//  Использовать фото машины (true) или водителя (false)
public let usePhoto = false
public let carPhoto = "car_photo"
public let driverPhoto = "driver_photo"
public let photoType = driverPhoto


/** CALLS SETTINGS **/
// Нужна ли возможность звонка водителю
public let useCalls = true
public let needDriverCall = true
public let needOfficeCall = true


/** OTHER SETTINGS **/
//Таймаут на повторную отправку смсъ
public let smsTimeout = 60
// нужно минимум две точки для создания заказа?
public let orderWithOnePoint = true
// Геокодинг
public let type_app = "client"
// размер налога, в процентах, 0 - не учитывать
public let taxfeePercentage = 0.0
// использовать ли реферальную систему
public let allowReferralSystem = true
// разрешить осталять отзыв без теста, с оценкой ниже 4
public let useReviewBlock = true
// радиус Blur для всех экранов
public let blurRadius : CGFloat = 7


/** ADDRESS DATAIL SETTINGS **/
// нужна ли квартира
public let needFlat = false
public let needStreet = true
public let needPorch = true
public let needComment = true

/** WITHES PANEL SETTINGS **/
public let needPreOrder = true
public let needWishes = true
public let needAddressDetail = true
public let needWishesPanel = needPreOrder && needWishes && needAddressDetail


/** PAYMENT SETTINGS **/
// разрешить оплату наличными?
public let allowPaymentInPerosnal = true
// разрешить оплату наличными?
public let allowPaymentInBonus = true
// разрешить оплату наличными?
public let allowPaymentInCompany = false
// разрешить оплату наличными?
public let allowPaymentInCash = true
// можно ли добавлять кредитные карты?
public let allowAddingCreditCard = true
// стандартная валюта
public let defCurrency = "RUB"
