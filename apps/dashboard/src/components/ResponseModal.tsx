import { useState, type FormEvent } from "react";

import type { SavedResponse } from "../types";
import { Field, Modal } from "./Modal";

interface ResponseModalProps {
  onClose: () => void;
  onSave: (response: SavedResponse) => void;
}

export function ResponseModal({ onClose, onSave }: ResponseModalProps) {
  const [prompt, setPrompt] = useState("");
  const [answer, setAnswer] = useState("");

  function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();

    onSave({
      id: Date.now(),
      prompt,
      answer,
      category: "Writing sample",
      updated: "just now",
    });
  }

  return (
    <Modal title="New response" onClose={onClose}>
      <form onSubmit={handleSubmit}>
        <Field label="Question or prompt">
          <input
            required
            value={prompt}
            onChange={(event) => setPrompt(event.target.value)}
            placeholder="What are you proudest of?"
          />
        </Field>

        <Field label="Your response">
          <textarea
            required
            rows={7}
            value={answer}
            onChange={(event) => setAnswer(event.target.value)}
            placeholder="Write in your own voice…"
          />
        </Field>

        <div className="modal-actions">
          <button type="button" className="button outline" onClick={onClose}>
            Cancel
          </button>

          <button className="button coral">Save response</button>
        </div>
      </form>
    </Modal>
  );
}
