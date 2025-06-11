// Test script to check if CORS proxy is working
async function testProxy() {
  console.log('Testing CORS proxy...');
  
  const testUrl = 'https://wolterskluwer.com';
  const proxyUrl = `https://api.allorigins.win/get?url=${encodeURIComponent(testUrl)}`;
  
  try {
    console.log(`Fetching: ${proxyUrl}`);
    const start = Date.now();
    
    const response = await fetch(proxyUrl);
    const elapsed = Date.now() - start;
    
    console.log(`Response status: ${response.status}`);
    console.log(`Time taken: ${elapsed}ms`);
    
    if (response.ok) {
      const data = await response.json();
      console.log(`Success! Content length: ${data.contents?.length || 0}`);
      console.log(`HTTP code: ${data.status?.http_code}`);
    } else {
      console.log(`Failed: ${response.statusText}`);
    }
    
  } catch (error) {
    console.error('Error:', error.message);
  }
}

testProxy();