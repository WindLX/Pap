export function setupCounter(element: HTMLButtonElement) {
  const apiUrl = 'http://localhost:8000';

  let counter = 0
  const setCounter = (count: number) => {
    counter = count
    element.innerHTML = `count is ${counter}`
  }
  element.addEventListener('click', async () => {
    setCounter(counter + 1);
    let response = await fetch(`${apiUrl}/hello`, {
      method: 'GET',
    });
    let msg = await response.text();
    console.log(msg);
    alert(msg);
  })
  setCounter(0)
}
