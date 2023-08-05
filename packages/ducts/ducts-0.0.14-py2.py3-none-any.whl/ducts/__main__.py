#!/usr/bin/env python3
# coding: utf-8

from .app import main
    
if __name__ == '__main__':
    import ducts.server
    import ducts.redis
    import ducts.backend.asr
    
    main(config_arg = 'config_{module}.ini'
         , callback_methods = [ducts.app.config, ducts.server.config, ducts.redis.config, ducts.backend.asr.config])
    
