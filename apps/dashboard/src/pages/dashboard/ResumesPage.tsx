import { Icon } from "../../components/Icon";
import { PageTitle } from "../../components/PageTitle";
import type { Resume } from "../../types";

interface ResumesPageProps {
  resumes: Resume[];
  setResumes: (resumes: Resume[]) => void;
}

export function ResumesPage({ resumes, setResumes }: ResumesPageProps) {
  function uploadResume(files: FileList | null) {
    const file = files?.[0];

    if (!file) {
      return;
    }

    const newResume: Resume = {
      id: Date.now(),
      name: file.name,
      size: `${Math.ceil(file.size / 1024)} KB`,
      updated: "Uploaded just now",
    };

    setResumes([newResume, ...resumes]);
  }

  function deleteResume(resumeId: number) {
    setResumes(resumes.filter((resume) => resume.id !== resumeId));
  }

  return (
    <>
      <PageTitle
        eyebrow="YOUR MATERIALS"
        title="Resumes"
        text="Keep every tailored version organized and ready to send."
      />

      <label className="upload-zone">
        <input
          type="file"
          accept=".pdf,.doc,.docx"
          onChange={(event) => uploadResume(event.target.files)}
        />

        <span>
          <Icon name="upload" size={24} />
        </span>

        <h3>
          Drop your resume here, or <u>browse</u>
        </h3>
        <p>PDF or DOCX · Max 10 MB</p>
      </label>

      <div className="section-head resume-heading">
        <h2>
          Your resumes <span>{resumes.length}</span>
        </h2>
      </div>

      <div className="resume-grid">
        {resumes.map((resume) => (
          <article className="panel resume-card" key={resume.id}>
            <div className="file-icon">PDF</div>

            <div>
              <h3>{resume.name}</h3>
              <p>
                {resume.size} · {resume.updated}
              </p>

              {resume.primary && (
                <span className="primary-tag">
                  <Icon name="check" size={13} />
                  Primary resume
                </span>
              )}
            </div>

            <button
              className="more"
              onClick={() => deleteResume(resume.id)}
              aria-label={`Delete ${resume.name}`}
            >
              •••
            </button>
          </article>
        ))}
      </div>
    </>
  );
}
