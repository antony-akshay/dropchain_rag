import axios from "axios";

const API_BASE_URL =
    import.meta.env.VITE_API_URL || "/api";

const api = axios.create({
    baseURL: API_BASE_URL,
});

export interface IngestResponse {
    message: string;
    chunks: number;
}

export interface QueryResponse {
    answer: string;
    sources: string[];
}

export async function uploadDocument(
    file: File
): Promise<IngestResponse> {
    const formData = new FormData();
    formData.append("file", file);

    const response = await api.post(
        "/ingest",
        formData
    );

    return response.data;
}

export async function queryDocument(
    question: string
): Promise<QueryResponse> {
    const response = await api.post(
        "/query",
        {
            query: question,
        }
    );

    return response.data;
}

export async function clearDocument(): Promise<{ message: string }> {
    const response = await api.post("/clear");
    return response.data;
}