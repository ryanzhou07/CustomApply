import type { Job, Resume, SavedResponse } from "../types";

export const initialJobs: Job[] = [
  {
    id: 1,
    company: "Linear",
    role: "Product Designer",
    location: "Remote",
    status: "Interview",
    applied: "Aug 28",
  },
  {
    id: 2,
    company: "Vercel",
    role: "Frontend Engineer",
    location: "New York, NY",
    status: "Applied",
    applied: "Aug 25",
  },
  {
    id: 3,
    company: "Notion",
    role: "Software Engineer",
    location: "San Francisco, CA",
    status: "Wishlist",
    applied: "—",
  },
  {
    id: 4,
    company: "Stripe",
    role: "Product Engineer",
    location: "Seattle, WA",
    status: "Rejected",
    applied: "Aug 12",
  },
  {
    id: 5,
    company: "Ramp",
    role: "Full Stack Engineer",
    location: "New York, NY",
    status: "Offer",
    applied: "Aug 8",
  },
];

export const initialResumes: Resume[] = [
  {
    id: 1,
    name: "Ryan_Zhou_Product_Resume.pdf",
    size: "248 KB",
    updated: "Updated 2 days ago",
    primary: true,
  },
  {
    id: 2,
    name: "Ryan_Zhou_Engineering_Resume.pdf",
    size: "224 KB",
    updated: "Updated Aug 18",
  },
];

export const initialResponses: SavedResponse[] = [
  {
    id: 1,
    category: "About you",
    prompt: "Tell me about yourself",
    answer:
      "I’m a product-minded engineer who enjoys turning ambiguous problems into simple, useful experiences. I work comfortably across design and engineering, and I care deeply about the details that make software feel intuitive.",
    updated: "2 days ago",
  },
  {
    id: 2,
    category: "Motivation",
    prompt: "Why do you want to work here?",
    answer:
      "I’m drawn to teams that pair ambitious technical problems with a genuine respect for the people using the product. I’m excited by the opportunity to learn quickly, contribute thoughtfully, and build work that matters.",
    updated: "Aug 21",
  },
];
