import { useCookies } from "vue3-cookies";

async function request(
  url,
  method = "GET",
  data = null,
  returnResponse = false,
  type = "json"
) {
  const { cookies } = useCookies();
  // url =
  //   (url.startsWith("http") ? "" : process.env.VUE_APP_API_SERVER_URL) +
  //   (url.startsWith("/") ? url.slice(1) : url);
  let options = {
    method: method,
    cache: "no-cache",
    headers: {
      Accept: "application/json",
      "X-CSRFToken": cookies.get("csrftoken"),
      Authorization: `Token ${cookies.get("authToken")}`,
    },
  };
  if (data !== null) {
    options.headers["Content-Type"] = "application/json";
    options.body = JSON.stringify(data);
  }
  try {
    const response = await fetch(url, options);
    if (returnResponse)
      return {
        isOk: response.ok,
        data: type === "blob" ? await response.blob() : await response.json(),
      };
    else if (response.ok) {
      return response.status === 204 ? "" : await response.json();
    } else {
      console.log(
        `[REQUEST] Error for url "${url}": ${response.status} ${response.statusText}`
      );
      throw Error(response.status);
    }
  } catch (err) {
    console.log(err);
    if (!isNaN(err.message.split(",")[0])) throw err;
    console.log(`[REQUEST] Error for url "${url}": Запрос заблокирован`);
    throw Error(600);
  }
}

async function requestAuth(
  url,
  method = "GET",
  data = null,
  returnResponse = false,
  type = "json"
) {
  const { cookies } = useCookies();
  // url =
  //   (url.startsWith("http") ? "" : process.env.VUE_APP_API_SERVER_URL) +
  //   (url.startsWith("/") ? url.slice(1) : url);
  let options = {
    method: method,
    cache: "no-cache",
    headers: {
      Accept: "application/json",
      "X-CSRFToken": cookies.get("csrftoken"),
    },
  };
  if (data !== null) {
    options.headers["Content-Type"] = "application/json";
    options.body = JSON.stringify(data);
  }
  try {
    const response = await fetch(url, options);
    if (returnResponse)
      return {
        isOk: response.ok,
        data: type === "blob" ? await response.blob() : await response.json(),
      };
    else if (response.ok) {
      return response.status === 204 ? "" : await response.json();
    } else {
      console.log(
        `[REQUEST] Error for url "${url}": ${response.status} ${response.statusText}`
      );
      throw Error(response.status);
    }
  } catch (err) {
    console.log(err);
    if (!isNaN(err.message.split(",")[0])) throw err;
    console.log(`[REQUEST] Error for url "${url}": Запрос заблокирован`);
    throw Error(600);
  }
}

export { request, requestAuth };
