import type { ReactNode } from "react";

interface PageTitleProps {
  eyebrow: string;
  title: string;
  text: string;
  action?: ReactNode;
}

export function PageTitle({ eyebrow, title, text, action }: PageTitleProps) {
  return (
    <div className="page-title">
      <div>
        <p className="kicker">{eyebrow}</p>
        <h1>{title}</h1>
        <p>{text}</p>
      </div>

      {action}
    </div>
  );
}
