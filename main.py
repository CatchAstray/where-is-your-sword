import socket
import requests
from urllib.parse import urlparse
from typing import Tuple, Dict
import socks

def check_http_proxy(proxy_url: str, timeout: int = 5) -> Tuple[bool, str]:
    """Check HTTP/HTTPS proxy"""
    try:
        proxies = {
            'http': proxy_url,
            'https': proxy_url
        }
        response = requests.get('http://httpbin.org/ip', proxies=proxies, timeout=timeout)
        return response.status_code == 200, "HTTP/HTTPS proxy working"
    except Exception as e:
        return False, f"HTTP/HTTPS proxy failed: {str(e)}"

def check_socks_proxy(proxy_url: str, timeout: int = 5) -> Tuple[bool, str]:
    """Check SOCKS4/SOCKS5 proxy"""
    try:
        parsed = urlparse(proxy_url)
        proxy_type = socks.SOCKS5 if 'socks5' in proxy_url.lower() else socks.SOCKS4
        
        socket.set_default_proxy(proxy_type, parsed.hostname, parsed.port)
        socket.socket = socks.socksocket
        
        response = requests.get('http://httpbin.org/ip', timeout=timeout)
        return response.status_code == 200, "SOCKS proxy working"
    except ImportError:
        return False, "PySocks not installed. Run: pip install pysocks"
    except Exception as e:
        return False, f"SOCKS proxy failed: {str(e)}"

def check_proxy(proxy_url: str, proxy_type: str = None, timeout: int = 5) -> Dict[str, any]:
    """
    Check if a proxy is working
    
    Args:
        proxy_url: Proxy URL (e.g., http://ip:port, socks5://ip:port)
        proxy_type: Type of proxy ('http', 'https', 'socks4', 'socks5'). Auto-detect if None
        timeout: Connection timeout in seconds
    
    Returns:
        Dictionary with status and message
    """
    if not proxy_url:
        return {'working': False, 'message': 'Proxy URL is empty'}
    
    proxy_type = proxy_type or proxy_url.split('://')[0].lower()
    
    if proxy_type in ['http', 'https']:
        working, message = check_http_proxy(proxy_url, timeout)
    elif proxy_type in ['socks4', 'socks5']:
        working, message = check_socks_proxy(proxy_url, timeout)
    else:
        return {'working': False, 'message': f'Unknown proxy type: {proxy_type}'}
    
    return {'working': working, 'message': message, 'type': proxy_type}

if __name__ == '__main__':
    # Example usage
    proxies = [
        'http://10.10.1.10:3128',
        'socks5://127.0.0.1:9050',
    ]
    
    for proxy in proxies:
        result = check_proxy(proxy)
        print(f"Proxy: {proxy}")
        print(f"Status: {result}\n")