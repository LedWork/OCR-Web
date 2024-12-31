import axios from "axios";

export async function checkSession(router) {
  try {
    const response = await axios.get('/api/auth/session', {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
      },
    })
    if (response.status !== 200) {
      router.push({name: 'login'})
    }
    else
      return false;
  } catch {
    router.push({name: 'login'})
  }
}

export async function adminCheckSession(router = null) {
  try {
    const response = await axios.get('/api/auth/session-admin', {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
      },
    })
    console.log(response)
    if (response.status !== 200) {
      router.push({name: 'login'})
    }
    else
      return true;
  } catch {
    router.push({name: 'login'})
  }
}

export function getCSRFToken() {
  if (document.cookie && document.cookie !== '') {
    const cookies = document.cookie.split(';')
    for (let cookie of cookies) {
      cookie = cookie.trim()
      let [cookieName, cookieValue] = cookie.split('=')
      if (cookieName == 'csrftoken') return cookieValue
    }
  }
  return null
}

export function changeOrientation() {
  if (window.screen.width > 768) {
    document.querySelector('.wrapper').classList.add('horizontal')
    document.querySelector('.wrapper').classList.remove('vertical')
  } else {
    document.querySelector('.wrapper').classList.remove('horizontal')
    document.querySelector('.wrapper').classList.add('vertical')
  }
}

export async function loadImage(imageCode) {
  try {
    console.log(imageCode);
    const response = await axios.get(`/api/image/${imageCode}`)
    console.log(response)
    if (response.data[0].photo) {
      return `data:image/jpeg;base64,${response.data[0].photo}`
    } else {
      console.error('No image found in the response')
    }
  } catch (error) {
    console.error('Error loading image:', error)
  }
}

export function parseGtParse(data, reverse=false) {
  const fieldOrder1 = [
    'Nazwisko',
    'Imię',
    'Data urodzenia',
    'V st.',
    'IV st.',
    'III st.',
    'II st.',
    'I st.',
  ]
  const fieldOrder2 = ['Nr', 'Data', 'ZR', 'Ilość oddanej krwi']

  const translations = {
    Surname: 'Nazwisko',
    'Name:': 'Imię',
    'Date of birth': 'Data urodzenia',
    Date: 'Data',
    'Donated blood': 'Ilość oddanej krwi',
  }

  const formattedData = {}

  const translationsMap = reverse
    ? Object.fromEntries(
      Object.entries(translations).map(([key, value]) => [value, key])
    )
    : translations;

  for (const [key, value] of Object.entries(data)) {
    const tKey = translationsMap[key] || key

    if (typeof value === 'object' && value !== null) {
      formattedData[tKey] = parseGtParse(value, fieldOrder2)
    } else {
      formattedData[tKey] = value
    }
  }

  const reorderFields = (data, order) => {
    const ordered = {}
    order.forEach((field) => {
      if (field in data) {
        ordered[field] = data[field]
      }
    })
    for (const key in data) {
      if (!(key in ordered)) {
        ordered[key] = data[key]
      }
    }
    return ordered
  }
  return reorderFields(formattedData, fieldOrder1)
}

export async function loadJsonData(data) {
  try {
    const imageCode = data.image_code
    const jsonData = parseGtParse(data.gt_parse)
    const cardData = data;

    return { imageCode, jsonData, cardData }
  } catch (error) {
    console.error('Error loading JSON:', error)
  }
}
