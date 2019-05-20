function getCSRFToken(skey){
	/*
	该函数由vip.qq.com网站抓包获取并改写而来
	需具备一定抓包基础知识
	*/
	var CSRF_TOKEN_KEY = 'tencentQQVIP123443safde&!%^%1282';
	var CSRF_TOKEN_SALT = 5381;
	var param = {};
	var salt = CSRF_TOKEN_SALT;
	var md5key = CSRF_TOKEN_KEY;
	var hash = [];
	var ASCIICode;
	var len = skey.length;
	hash.push((salt << 5));
	for (var i = 0; i < len; ++i) {
		ASCIICode = skey.charAt(i).charCodeAt(0);
		hash.push((salt << 5) + ASCIICode);
		salt = ASCIICode;
	}
	return (hash.join('') + md5key);	
}