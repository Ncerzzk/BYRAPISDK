
import byrapi
token = ''

API = byrapi.Byr(token)

#print(API.get_user_info('piegg'))
#print(API.get_sections(1))
#print(API.get_board('python'))
#print(API.get_article('python', 1))
#print(API.get_thread('python', 1))
#print(API.post_article('fujian', '中文测试', 'estttest'))
#print(API.forward_article('fujian','458049','ncer'))
#print(API.get_attachment('fujian', '455650')) # 只能获得当前授权用户发的文章的附件信息
"""f=open('index.html','rb')
print(API.post_attachment('fujian',f,'458059'))
f.close()
"""
#print(API.cross_article('fujian', '458049', 'python'))
#print(API.update_article('fujian', '458049' ,'change title' ,'change coneent'))
#print(API.del_article('fujian','458049'))




#print(API.del_attachment('fujian','index.html','458050'))
#print(API.get_info_by_box('inbox'))
#print(API.get_mailbox_info())
#print(API.get_mailinfo('inbox', '1'))
#print(API.post_mail('ncer'))
#print(API.forward_mail('inbox','1','ncer'))
#print(API.reply_mail('inbox','1'))
#print(API.del_mail('inbox','1'))
#print(API.get_favorite())
#print(API.add_favoriet('ACM_ICPC'))
#print(API.del_favorite('ACM_ICPC'))
#print(API.get_collection())
#print(API.add_collection('fujian','458016'))
#print(API.del_collection('458016'))
#print(API.search_board('fuji')) #may have some problem
#print(API.search_article('python','','问题'))
#print(API.search_threads('python','问题'))
#print(API.get_refer('at'))
#print(API.get_refer_info('reply'))
#print(API.set_read('at','1'))
#print(API.del_refer('at',1))
#print(API.get_top_ten())
#print(API.get_recommend())
#print(API.get_section_hot('1'))
#print(API.get_blacklist())
#print(API.add_black('piegg'))
#print(API.del_black('piegg'))
#print(API.get_vote('6073'))
#print(API.get_vote_list('list','hbdxych'))
#print(API.vote('6073','35979'))
