import { useState } from "react";

import { Icon } from "../components/Icon";
import { JobModal } from "../components/JobModal";
import { Logo } from "../components/Logo";
import { ResponseModal } from "../components/ResponseModal";
import {
  initialJobs,
  initialResponses,
  initialResumes,
} from "../data/initialData";
import { useStored } from "../hooks/useStored";
import type { DashboardView, Job, Resume, SavedResponse } from "../types";
import { HomePage } from "./dashboard/HomePage";
import { JobsPage } from "./dashboard/JobsPage";
import { ResponsesPage } from "./dashboard/ResponsesPage";
import { ResumesPage } from "./dashboard/ResumesPage";

interface DashboardPageProps {
  onLogout: () => void;
}

const viewTitles: Record<DashboardView, string> = {
  home: "Overview",
  jobs: "Job tracker",
  resumes: "Resumes",
  responses: "Responses",
};

const dashboardViews = Object.keys(viewTitles) as DashboardView[];

export function DashboardPage({ onLogout }: DashboardPageProps) {
  const [view, setView] = useState<DashboardView>("home");
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);
  const [jobModalOpen, setJobModalOpen] = useState(false);
  const [responseModalOpen, setResponseModalOpen] = useState(false);

  const [jobs, setJobs] = useStored<Job[]>("ca-jobs", initialJobs);
  const [resumes, setResumes] = useStored<Resume[]>(
    "ca-resumes",
    initialResumes,
  );
  const [responses, setResponses] = useStored<SavedResponse[]>(
    "ca-responses",
    initialResponses,
  );

  function selectView(nextView: DashboardView) {
    setView(nextView);
    setMobileMenuOpen(false);
  }

  function saveJob(job: Job) {
    setJobs([job, ...jobs]);
    setJobModalOpen(false);
  }

  function saveResponse(response: SavedResponse) {
    setResponses([response, ...responses]);
    setResponseModalOpen(false);
  }

  return (
    <div className="app-shell">
      <aside className={`sidebar ${mobileMenuOpen ? "open" : ""}`}>
        <Logo />

        <button
          className="close-mobile"
          onClick={() => setMobileMenuOpen(false)}
          aria-label="Close navigation"
        >
          ×
        </button>

        <p className="side-label">WORKSPACE</p>

        {dashboardViews.map((dashboardView) => (
          <button
            className={view === dashboardView ? "active" : ""}
            key={dashboardView}
            onClick={() => selectView(dashboardView)}
          >
            <Icon name={dashboardView} />
            <span>{viewTitles[dashboardView]}</span>
            {dashboardView === "jobs" && <small>{jobs.length}</small>}
          </button>
        ))}

        <div className="side-bottom">
          <div className="tip">
            <Icon name="spark" />
            <b>Keep the momentum</b>
            <p>Add every role you’re considering. Small steps count.</p>
          </div>

          <button className="profile" onClick={onLogout}>
            <span>RZ</span>
            <p>
              <b>Ryan Zhou</b>
              <small>ryan@example.com</small>
            </p>
            <i>⌄</i>
          </button>
        </div>
      </aside>

      <main className="workspace">
        <header className="topbar">
          <button
            className="hamburger"
            onClick={() => setMobileMenuOpen(true)}
            aria-label="Open navigation"
          >
            <Icon name="menu" />
          </button>

          <span>{viewTitles[view]}</span>

          <div>
            <button className="icon-button" aria-label="Search">
              <Icon name="search" />
            </button>
            <button className="avatar">RZ</button>
          </div>
        </header>

        <div className="page">
          {view === "home" && (
            <HomePage
              jobs={jobs}
              setView={setView}
              onAdd={() => setJobModalOpen(true)}
            />
          )}

          {view === "jobs" && (
            <JobsPage
              jobs={jobs}
              setJobs={setJobs}
              onAdd={() => setJobModalOpen(true)}
            />
          )}

          {view === "resumes" && (
            <ResumesPage resumes={resumes} setResumes={setResumes} />
          )}

          {view === "responses" && (
            <ResponsesPage
              responses={responses}
              setResponses={setResponses}
              onAdd={() => setResponseModalOpen(true)}
            />
          )}
        </div>
      </main>

      {jobModalOpen && (
        <JobModal onClose={() => setJobModalOpen(false)} onSave={saveJob} />
      )}

      {responseModalOpen && (
        <ResponseModal
          onClose={() => setResponseModalOpen(false)}
          onSave={saveResponse}
        />
      )}
    </div>
  );
}
