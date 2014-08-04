$(document).ready(function(){
	$(".mainNavigationDetails").hide();
	$(".projectSettingDetails").hide();
	$(".statusLogs").hide();
	$(".mainNavigation").click(function(){
		$(".projectSettingDetails").slideUp();
		$(".statusLogs").slideUp();
		$(".mainNavigationDetails").slideToggle();
		});
	$(".projectSetting").click(function(){
		$(".mainNavigationDetails").slideUp();
		$(".projectSettingDetails").slideToggle();
		});	
		
	$(".status").click(function(){
		$(".mainNavigationDetails").slideUp();
		$(".statusLogs").slideToggle();
		});	
	
	});
statusLog
