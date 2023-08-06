import logging

def create_logger(name, save):
    # -- create the logging
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    # -- create a handler
    fh = logging.FileHandler(save)
    fh.setLevel(logging.DEBUG)

    # -- create a control
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)

    # -- set the format
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)

    # -- set the handle
    logger.addHandler(fh)
    logger.addHandler(ch)
    
    return logger
    

if __name__ == "__main__":
    logger = create_logger("train","test.log")
    logger.info('foorbar')
    logger.info('test')