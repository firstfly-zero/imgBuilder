import axios from 'axios';

export function addWxBotApi(params: any) {
    return axios.post('/api/v1/robot/addWxBot', params);
}

export function getWxBotDefaultConfig() {
    return axios.get('/api/v1/robot/getWxBotDefaultConfig');
}

export interface BotCommandData {
    keyword: string;
    default_params: {
        "prompt": string;
        "steps": number;
        "cfg_scale": number;
        "batch_size": number;
        "sampler_name": string;
        "negative_prompt": string;
        "denoising_stength": number;
    }
    type: string;
}
export function addBotCommandApi(params: BotCommandData) {
    return axios.post('/dcgallery/bot/addbotcommand', params);
}

export interface LarkBotData {
    app_id: string;
    app_secret: string;
}
export function addLarkBotApi(params: LarkBotData) {
    return axios.post('/api/v1/robot/addLarkBot', params);
}
