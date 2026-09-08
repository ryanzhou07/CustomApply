const iconPaths: Record<string, string> = {
  home: "M3 10.5 12 3l9 7.5M5 9v11h14V9M9 20v-6h6v6",
  jobs: "M9 6V4h6v2M4 7h16a1 1 0 0 1 1 1v11H3V8a1 1 0 0 1 1-1Zm-1 5h8",
  resumes: "M6 3h9l4 4v14H6V3Zm9 0v5h4M9 13h6M9 17h6",
  responses:
    "M5 4h14a2 2 0 0 1 2 2v10a2 2 0 0 1-2 2H9l-5 3v-3a2 2 0 0 1-1-2V6a2 2 0 0 1 2-2Zm3 5h8m-8 4h6",
  plus: "M12 5v14M5 12h14",
  search: "m21 21-4.3-4.3m2.3-5.2a7.5 7.5 0 1 1-15 0 7.5 7.5 0 0 1 15 0Z",
  arrow: "m9 18 6-6-6-6",
  check: "m5 12 4 4L19 6",
  upload: "M12 16V4m0 0L7 9m5-5 5 5M5 15v5h14v-5",
  trash: "M4 7h16M9 7V4h6v3m3 0-1 14H7L6 7m4 4v6m4-6v6",
  menu: "M4 7h16M4 12h16M4 17h16",
  spark: "m12 3 1.5 5.5L19 10l-5.5 1.5L12 17l-1.5-5.5L5 10l5.5-1.5L12 3Z",
};

interface IconProps {
  name: string;
  size?: number;
}

export function Icon({ name, size = 20 }: IconProps) {
  return (
    <svg
      width={size}
      height={size}
      viewBox="0 0 24 24"
      fill="none"
      stroke="currentColor"
      strokeWidth="1.8"
      strokeLinecap="round"
      strokeLinejoin="round"
      aria-hidden
    >
      <path d={iconPaths[name]} />
    </svg>
  );
}
