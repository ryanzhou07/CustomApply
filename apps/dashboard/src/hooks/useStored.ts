import { useState } from "react";

export function useStored<T>(
  key: string,
  fallback: T,
): [T, (value: T) => void] {
  const [value, setValue] = useState<T>(() => {
    try {
      return JSON.parse(localStorage.getItem(key) ?? "") || fallback;
    } catch {
      return fallback;
    }
  });

  function saveValue(nextValue: T) {
    setValue(nextValue);
    localStorage.setItem(key, JSON.stringify(nextValue));
  }

  return [value, saveValue];
}
