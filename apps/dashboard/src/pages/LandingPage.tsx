import { Icon } from "../components/Icon";
import { Logo } from "../components/Logo";
import { Status } from "../components/Status";
import { initialJobs } from "../data/initialData";

interface LandingPageProps {
  onStart: () => void;
  onLogin: () => void;
}

const navigationPreview = [
  { label: "Overview", icon: "home" },
  { label: "Job tracker", icon: "jobs" },
  { label: "Resumes", icon: "resumes" },
  { label: "Responses", icon: "responses" },
];

export function LandingPage({ onStart, onLogin }: LandingPageProps) {
  return (
    <div className="landing">
      <header className="public-nav">
        <Logo />

        <nav>
          <a href="#features">How it works</a>
          <a href="#features">Features</a>
          <button className="text-button" onClick={onLogin}>
            Sign in
          </button>
          <button className="button dark small" onClick={onStart}>
            Get started <span>→</span>
          </button>
        </nav>
      </header>

      <main>
        <section className="hero">
          <div className="eyebrow">
            <span>✦</span>
            Your job search, thoughtfully organized
          </div>

          <h1>
            Make your next move
            <br />
            <em>with intention.</em>
          </h1>

          <p>
            One calm, focused place for every application, resume, and story—so
            you can spend less time organizing and more time moving forward.
          </p>

          <div className="hero-actions">
            <button className="button coral" onClick={onStart}>
              Start your search <span>→</span>
            </button>
            <a href="#features">
              See how it works <span>↓</span>
            </a>
          </div>

          <div className="trust">
            <div className="avatars">
              <span>R</span>
              <span>M</span>
              <span>A</span>
            </div>
            <p>
              <b>Built for real job seekers</b>
              <br />
              Private, focused, and always yours.
            </p>
          </div>
        </section>

        <DashboardPreview />

        <section className="features" id="features">
          <p className="kicker">EVERYTHING IN ITS PLACE</p>
          <h2>
            A better system for
            <br />
            your next chapter.
          </h2>

          <div className="feature-grid">
            <Feature number="01" icon="jobs" title="Track every opportunity">
              Keep roles, deadlines, contacts, and next steps together—without
              another messy spreadsheet.
            </Feature>
            <Feature number="02" icon="resumes" title="Your best work, ready">
              Store tailored resumes and writing samples so the right version is
              always close at hand.
            </Feature>
            <Feature number="03" icon="responses" title="Tell your story well">
              Build a thoughtful response library and stop rewriting the same
              answers from scratch.
            </Feature>
          </div>
        </section>
      </main>

      <footer>
        <Logo light />
        <p>Less busywork. More meaningful applications.</p>
        <span>© 2026 CustomApply</span>
      </footer>
    </div>
  );
}

function DashboardPreview() {
  return (
    <section className="preview-wrap">
      <div className="preview-window">
        <div className="preview-bar">
          <i />
          <i />
          <i />
          <span>customapply.co/dashboard</span>
        </div>

        <div className="preview-body">
          <aside>
            <Logo />
            <small>WORKSPACE</small>
            {navigationPreview.map((item, index) => (
              <div className={index === 0 ? "active" : ""} key={item.label}>
                <Icon name={item.icon} size={16} />
                {item.label}
              </div>
            ))}
          </aside>

          <div className="preview-content">
            <p className="muted">THURSDAY, SEPTEMBER 3</p>
            <h2>Good morning, Ryan.</h2>
            <p className="muted">Here’s how your search is moving.</p>

            <div className="mini-stats">
              <article>
                <b>12</b>
                <span>Applications</span>
              </article>
              <article>
                <b>3</b>
                <span>Interviews</span>
              </article>
              <article>
                <b>1</b>
                <span>Offer</span>
              </article>
            </div>

            <div className="preview-list">
              <b>Recently active</b>
              {initialJobs.slice(0, 3).map((job) => (
                <div key={job.id}>
                  <span className="company-badge">{job.company[0]}</span>
                  <p>
                    <b>{job.role}</b>
                    <small>{job.company}</small>
                  </p>
                  <Status value={job.status} />
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}

interface FeatureProps {
  number: string;
  icon: string;
  title: string;
  children: string;
}

function Feature({ number, icon, title, children }: FeatureProps) {
  return (
    <article>
      <span>{number}</span>
      <Icon name={icon} size={25} />
      <h3>{title}</h3>
      <p>{children}</p>
    </article>
  );
}
