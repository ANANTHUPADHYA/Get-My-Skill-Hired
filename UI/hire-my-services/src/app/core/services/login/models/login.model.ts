
export  interface LoginResponse {
        status: number; 
        success: boolean;
        data: {
            idToken: string;
            accessToken: string;
            refreshToken: string;
            profile: {
                usertype: string;
                uid: string; 
                username: string; 
                email: string;
                firstname: string; 
                lastname: string;
                phone: string;
                address: string; 
                city: string;
                days: string[];
                time: string;
                skillset: 
                    {
                        name: string;
                        price: number;
                    }[]
                
            }
        }
  }
  
  export interface UserParams {
      firstName: string;
      lastName: string;
      address: string;
      area: string;
      city: string;
      phone: string;
      userType: string;
      days?: string[];
      time?: string;
      skillSet?: {
          name: string;
          price: number;
      }[]
  }
  
  export interface RegisterResponse {
    success: boolean;
    data?: {
      message: string;
      accessToken: string;
    };
    
    
  }
  
  