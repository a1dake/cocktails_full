export const sleep = async (seconds) => {
  return new Promise((resolve) => setTimeout(resolve, seconds * 1000));
};

export function getDurationName(duration) {
  if (duration % 100 >= 5 && duration % 100 <= 20) return `${duration} дней`;
  else if ([2, 3, 4].includes(duration % 10)) return `${duration} дня`;
  else if (duration % 10 === 1) return `${duration} день`;
  else return `${duration} дней`;
}

export const objectsEqual = (object1, object2) => {
  const keys1 = Object.keys(object1);
  const keys2 = Object.keys(object2);
  if (keys1.length !== keys2.length) {
    return false;
  }
  for (let key of keys1) {
    if (object1[key] !== object2[key]) {
      if (
        typeof object1[key] === "object" &&
        typeof object2[key] === "object"
      ) {
        if (!objectsEqual(object1[key], object2[key])) return false;
        continue;
      }
      return false;
    }
  }
  return true;
};
