import type { JobStatus } from "../types";

interface StatusProps {
  value: JobStatus;
}

export function Status({ value }: StatusProps) {
  return (
    <span className={`status ${value.toLowerCase()}`}>
      <i />
      {value}
    </span>
  );
}
