
export interface UserProfileResponse {
    success: boolean;
    data?: {
        message: string;
    };
    error?: {
        message: string;
    }
}

export interface UploadImageResponse {
    success: boolean;
    data?: {
        message: string;
    };
    error?: {
        message: string;
    }
}