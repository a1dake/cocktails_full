import { useCookies } from "vue3-cookies";
import axios from "axios";

async function request(url, options = {}) {
  const method = options.method ? options.method.toLowerCase() : "get";
  const data = options.data ?? null;
  const type = options.type ?? "json";
  const params = options.params ?? null;
  const { cookies } = useCookies();
  url =
    (url.startsWith("http") ? "" : process.env.VUE_APP_API_SERVER_URL) +
    (url.startsWith("/") ? url.slice(1) : url);
  if (params) url += "?" + new URLSearchParams(params).toString();
  const fetchOptions = {
    mode: process.env.VUE_APP_FETCH_MODE,
    credentials: process.env.VUE_APP_FETCH_CREDENTIALS,
    cache: "no-cache",
    headers: {
      Accept: "application/json",
      "X-CSRFToken": cookies.get("csrftoken"),
    },
  };
  if (data !== null) {
    fetchOptions.headers["Content-Type"] =
      type === "json" ? "application/json" : "multipart-form-data";
  }
  try {
    const response = await axios({
      method: method,
      url: url,
      data: type === "file" ? data : { ...data },
      ...fetchOptions,
    });
    if (![200, 201, 202, 204].includes(response.status)) {
      console.log(
        `[REQUEST] Error for url "${url}": ${response.status} ${response.statusText}`
      );
    }
    return response.data;
  } catch (err) {
    console.log(err);
    console.log(`[REQUEST] Error for url "${url}": Запрос заблокирован`);
    return err.response.data;
  }
}
export { request };
