import { useState, type FormEvent } from "react";

import type { Job, JobStatus } from "../types";
import { Field, Modal } from "./Modal";

interface JobModalProps {
  onClose: () => void;
  onSave: (job: Job) => void;
}

export function JobModal({ onClose, onSave }: JobModalProps) {
  const [form, setForm] = useState({
    company: "",
    role: "",
    location: "",
    status: "Wishlist" as JobStatus,
  });

  function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();

    onSave({
      id: Date.now(),
      ...form,
      applied: form.status === "Wishlist" ? "—" : "Sep 3",
    });
  }

  return (
    <Modal title="Add an opportunity" onClose={onClose}>
      <form onSubmit={handleSubmit}>
        <Field label="Company">
          <input
            required
            value={form.company}
            onChange={(event) =>
              setForm({ ...form, company: event.target.value })
            }
            placeholder="e.g. Figma"
          />
        </Field>

        <Field label="Role">
          <input
            required
            value={form.role}
            onChange={(event) => setForm({ ...form, role: event.target.value })}
            placeholder="e.g. Product Engineer"
          />
        </Field>

        <Field label="Location">
          <input
            required
            value={form.location}
            onChange={(event) =>
              setForm({ ...form, location: event.target.value })
            }
            placeholder="Remote or city"
          />
        </Field>

        <Field label="Status">
          <select
            value={form.status}
            onChange={(event) =>
              setForm({ ...form, status: event.target.value as JobStatus })
            }
          >
            {["Wishlist", "Applied", "Interview", "Offer", "Rejected"].map(
              (status) => (
                <option key={status}>{status}</option>
              ),
            )}
          </select>
        </Field>

        <div className="modal-actions">
          <button type="button" className="button outline" onClick={onClose}>
            Cancel
          </button>

          <button className="button coral">Save opportunity</button>
        </div>
      </form>
    </Modal>
  );
}
