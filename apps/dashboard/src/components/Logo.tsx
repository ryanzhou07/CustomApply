interface LogoProps {
  light?: boolean;
}

export function Logo({ light = false }: LogoProps) {
  return (
    <div className={`logo ${light ? "light" : ""}`}>
      <span className="logo-mark">
        <span />
      </span>

      <span>CustomApply</span>
    </div>
  );
}
