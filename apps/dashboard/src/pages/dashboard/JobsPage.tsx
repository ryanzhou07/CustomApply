import { useState } from "react";

import { Icon } from "../../components/Icon";
import { PageTitle } from "../../components/PageTitle";
import type { Job, JobStatus } from "../../types";

interface JobsPageProps {
  jobs: Job[];
  setJobs: (jobs: Job[]) => void;
  onAdd: () => void;
}

const filters = ["All", "Wishlist", "Applied", "Interview", "Offer"];
const statuses: JobStatus[] = [
  "Wishlist",
  "Applied",
  "Interview",
  "Offer",
  "Rejected",
];

export function JobsPage({ jobs, setJobs, onAdd }: JobsPageProps) {
  const [filter, setFilter] = useState("All");

  const visibleJobs =
    filter === "All" ? jobs : jobs.filter((job) => job.status === filter);

  function updateStatus(jobId: number, status: JobStatus) {
    setJobs(jobs.map((job) => (job.id === jobId ? { ...job, status } : job)));
  }

  function deleteJob(jobId: number) {
    setJobs(jobs.filter((job) => job.id !== jobId));
  }

  return (
    <>
      <PageTitle
        eyebrow="OPPORTUNITIES"
        title="Job tracker"
        text="Every role you’re considering, all in one place."
        action={
          <button className="button coral" onClick={onAdd}>
            <Icon name="plus" size={17} />
            Add opportunity
          </button>
        }
      />

      <div className="toolbar">
        <div className="tabs">
          {filters.map((item) => (
            <button
              className={filter === item ? "active" : ""}
              onClick={() => setFilter(item)}
              key={item}
            >
              {item}
            </button>
          ))}
        </div>

        <span>{visibleJobs.length} opportunities</span>
      </div>

      <section className="panel table-wrap">
        <table>
          <thead>
            <tr>
              <th>COMPANY &amp; ROLE</th>
              <th>LOCATION</th>
              <th>STATUS</th>
              <th>DATE ADDED</th>
              <th aria-label="Actions" />
            </tr>
          </thead>

          <tbody>
            {visibleJobs.map((job) => (
              <tr key={job.id}>
                <td>
                  <span className="company-badge">{job.company[0]}</span>
                  <p>
                    <b>{job.role}</b>
                    <small>{job.company}</small>
                  </p>
                </td>
                <td>{job.location}</td>
                <td>
                  <select
                    value={job.status}
                    onChange={(event) =>
                      updateStatus(job.id, event.target.value as JobStatus)
                    }
                  >
                    {statuses.map((status) => (
                      <option key={status}>{status}</option>
                    ))}
                  </select>
                </td>
                <td>{job.applied}</td>
                <td>
                  <button
                    className="icon-button"
                    onClick={() => deleteJob(job.id)}
                    aria-label={`Delete ${job.role} at ${job.company}`}
                  >
                    <Icon name="trash" size={17} />
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </section>
    </>
  );
}
