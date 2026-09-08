import { Icon } from "../../components/Icon";
import { Status } from "../../components/Status";
import type { DashboardView, Job, JobStatus } from "../../types";

interface HomePageProps {
  jobs: Job[];
  setView: (view: DashboardView) => void;
  onAdd: () => void;
}

export function HomePage({ jobs, setView, onAdd }: HomePageProps) {
  function countJobs(status: JobStatus) {
    return jobs.filter((job) => job.status === status).length;
  }

  const applicationsSent =
    countJobs("Applied") +
    countJobs("Interview") +
    countJobs("Offer") +
    countJobs("Rejected");

  return (
    <>
      <div className="welcome">
        <p className="kicker">THURSDAY, SEPTEMBER 3</p>
        <h1>Good morning, Ryan.</h1>
        <p>Here’s how your job search is moving.</p>
      </div>

      <div className="stat-grid">
        <Stat
          label="Total opportunities"
          value={jobs.length}
          note="Across your pipeline"
        />
        <Stat
          label="Applications sent"
          value={applicationsSent}
          note="2 this week"
          accent
        />
        <Stat
          label="Interviews"
          value={countJobs("Interview")}
          note="One coming up"
        />
        <Stat
          label="Offers"
          value={countJobs("Offer")}
          note="You’re doing great"
        />
      </div>

      <div className="home-grid">
        <section className="panel recent">
          <div className="section-head">
            <div>
              <p className="kicker">YOUR PIPELINE</p>
              <h2>Recently active</h2>
            </div>

            <button className="link-button" onClick={() => setView("jobs")}>
              View all
              <Icon name="arrow" size={16} />
            </button>
          </div>

          {jobs.slice(0, 4).map((job) => (
            <div className="job-row" key={job.id}>
              <span className="company-badge">{job.company[0]}</span>

              <div>
                <b>{job.role}</b>
                <p>
                  {job.company} · {job.location}
                </p>
              </div>

              <Status value={job.status} />
              <small>{job.applied}</small>
            </div>
          ))}
        </section>

        <aside className="panel next">
          <p className="kicker">NEXT UP</p>
          <h2>Keep things moving</h2>

          <div className="progress-ring">
            <span>
              <b>{Math.min(100, jobs.length * 12)}%</b>
              <small>weekly goal</small>
            </span>
          </div>

          <p>Add two more opportunities to reach your target for the week.</p>

          <button className="button dark full" onClick={onAdd}>
            <Icon name="plus" size={17} />
            Add opportunity
          </button>
        </aside>
      </div>
    </>
  );
}

interface StatProps {
  label: string;
  value: number;
  note: string;
  accent?: boolean;
}

function Stat({ label, value, note, accent = false }: StatProps) {
  return (
    <article className={`stat-card ${accent ? "accent" : ""}`}>
      <p>{label}</p>
      <b>{value}</b>
      <small>
        <span>↗</span>
        {note}
      </small>
    </article>
  );
}
