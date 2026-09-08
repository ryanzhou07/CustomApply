import { Icon } from "../../components/Icon";
import { PageTitle } from "../../components/PageTitle";
import type { SavedResponse } from "../../types";

interface ResponsesPageProps {
  responses: SavedResponse[];
  setResponses: (responses: SavedResponse[]) => void;
  onAdd: () => void;
}

export function ResponsesPage({
  responses,
  setResponses,
  onAdd,
}: ResponsesPageProps) {
  function deleteResponse(responseId: number) {
    setResponses(responses.filter((response) => response.id !== responseId));
  }

  return (
    <>
      <PageTitle
        eyebrow="YOUR STORY BANK"
        title="Responses"
        text="Save thoughtful answers once. Adapt them confidently every time."
        action={
          <button className="button coral" onClick={onAdd}>
            <Icon name="plus" size={17} />
            New response
          </button>
        }
      />

      <div className="response-intro">
        <Icon name="spark" />

        <div>
          <b>Your voice, ready when you need it.</b>
          <p>
            Build a library of your best stories, examples, and writing samples.
            CustomApply will help you find the right starting point for every
            application.
          </p>
        </div>
      </div>

      <div className="response-grid">
        {responses.map((response) => (
          <article className="panel response-card" key={response.id}>
            <div>
              <span>{response.category}</span>
              <button
                className="more"
                onClick={() => deleteResponse(response.id)}
                aria-label={`Delete ${response.prompt}`}
              >
                •••
              </button>
            </div>

            <h3>{response.prompt}</h3>
            <p>{response.answer}</p>

            <footer>
              <small>Updated {response.updated}</small>
              <button>
                Edit response
                <Icon name="arrow" size={14} />
              </button>
            </footer>
          </article>
        ))}

        <button className="new-card" onClick={onAdd}>
          <span>
            <Icon name="plus" />
          </span>
          <b>Add a new response</b>
          <small>Capture a story or writing sample</small>
        </button>
      </div>
    </>
  );
}
