import format from "date-fns/format";
import parse from "date-fns/parse";
import { ru } from "date-fns/locale";

const BASE_DATE = new Date();
const STORE_PYTHON_FORMAT = "%Y-%m-%d %H:%M:%S";

function getFormatStringFromPython(pythonFormat) {
  const format_map = {
    "%Y": "y",
    "%y": "yy",
    "%m": "MM",
    "%a": "EEEEEE",
    "%A": "EEEE",
    "%d": "dd",
    "%H": "HH",
    "%M": "mm",
    "%S": "ss",
    "%%": "%",
    "%x": "dd.MM.y",
    "%X": "HH:mm:ss",
    "%c": "dd.MM.y HH:mm:ss",
    "%w": "i",
    "%b": "MMM",
    "%B": "LLLL",
    "%j": "DDD",
  };
  var result = Object.entries(format_map)
    .reduce(
      (p, [python, js]) => p.split(python).join(`'${js}'`),
      `'${pythonFormat}'`
    )
    .split("''")
    .join("");
  return result;
}

function formatDate(date, pythonFormat = STORE_PYTHON_FORMAT) {
  var jsFormat = getFormatStringFromPython(pythonFormat);
  try {
    return format(date, jsFormat, { locale: ru });
  } catch (error) {
    console.error(error);
    return null;
  }
}

function parseDate(
  dateString,
  pythonFormat = STORE_PYTHON_FORMAT,
  baseDate = BASE_DATE
) {
  if (!dateString) return null;
  var jsFormat = getFormatStringFromPython(pythonFormat);
  return parse(dateString, jsFormat, baseDate, {
    locale: ru,
  });
}

function NOK(arr) {
  var n = arr.length,
    a = Math.abs(arr[0]);
  for (var i = 1; i < n; i++) {
    var b = Math.abs(arr[i]),
      c = a;
    while (a && b) {
      a > b ? (a %= b) : (b %= a);
    }
    a = Math.abs(c * arr[i]) / (a + b);
  }
  return a;
}

export { getFormatStringFromPython, formatDate, parseDate, NOK };
