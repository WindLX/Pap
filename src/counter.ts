export function setupCounter(element: HTMLButtonElement) {
  const apiUrl = 'http://localhost:8000/';

  let counter = 0
  const setCounter = (count: number) => {
    counter = count
    element.innerHTML = `count is ${counter}`
  }
  element.addEventListener('click', () => {
    setCounter(counter + 1);

    // 发送 POST 请求
    fetch(`${apiUrl}/send-message`, {
      method: 'GET',
    })
  })
  setCounter(0)
}
