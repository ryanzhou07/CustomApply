export type Route = "landing" | "login" | "app";

export type DashboardView = "home" | "jobs" | "resumes" | "responses";

export type JobStatus =
  "Wishlist" | "Applied" | "Interview" | "Offer" | "Rejected";

export interface Job {
  id: number;
  company: string;
  role: string;
  location: string;
  status: JobStatus;
  applied: string;
}

export interface Resume {
  id: number;
  name: string;
  size: string;
  updated: string;
  primary?: boolean;
}

export interface SavedResponse {
  id: number;
  prompt: string;
  answer: string;
  category: string;
  updated: string;
}
